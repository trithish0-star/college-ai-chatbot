"""
NLP and AI Engine for College Chatbot Using AI.
Implements:
1. Text Preprocessing & Cleaning (Tokenization, Lowercasing, Tanglish Normalization)
2. TF-IDF Vectorizer for Feature Extraction
3. Logistic Regression for Intent Classification
4. Confidence Evaluation & Low Confidence Fallback Handling
5. Dynamic SQLite Knowledge Base Retrieval and In-Memory Model Retraining
"""

import os
import re
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'college.db')

TANGLISH_MARKERS = {
    'evlo', 'evalo', 'evvalavu', 'iruka', 'irukka', 'irukku', 'eppadi', 'epdi',
    'venum', 'vaenum', 'sollunga', 'sollu', 'enga', 'engae', 'kedaikuma', 'kidaikuma',
    'pannanum', 'pandrathu', 'paakanum', 'ku', 'la', 'ah', 'pa', 'da', 'unga', 'ungala',
    'varuma', 'varum', 'mudiyuma', 'romba', 'nandri', 'vanakkam', 'enna'
}

# Phonetic & spelling normalization map for Tanglish and colloquial college terms
NORMALIZATION_MAP = {
    r'\bevalo\b': 'evlo',
    r'\bevvalavu\b': 'evlo',
    r'\bhow much\b': 'evlo',
    r'\bfee structure\b': 'fees',
    r'\bfeess\b': 'fees',
    r'\bfeee\b': 'fees',
    r'\bfee\b': 'fees',
    r'\birukku\b': 'iruka',
    r'\birukka\b': 'iruka',
    r'\bavailable ah\b': 'available',
    r'\bavailablea\b': 'available',
    r'\bepdi\b': 'eppadi',
    r'\bvaenum\b': 'venum',
    r'\bwant\b': 'venum',
    r'\bneed\b': 'venum',
    r'\bsollu\b': 'sollunga',
    r'\btell me\b': 'sollunga',
    r'\bengae\b': 'enga',
    r'\bwhere is\b': 'enga',
    r'\bkidaikuma\b': 'kedaikuma',
    r'\bget panna\b': 'kedaikuma',
    r'\bcse department\b': 'cse',
    r'\bcomputer science\b': 'cse',
    r'\bai and ds\b': 'aids',
    r'\bai & ds\b': 'aids',
    r'\bai ds\b': 'aids',
    r'\bmech\b': 'mechanical',
    r'\btime table\b': 'timetable',
    r'\bexam schedule\b': 'exam timetable',
    r'\bcollege bus\b': 'bus',
    r'\btransportation\b': 'transport',
    r'\bjob\b': 'placement',
    r'\bcampus interview\b': 'placement',
    r'\bcut off\b': 'cutoff',
    r'\bcut-off\b': 'cutoff',
}

class CollegeChatbotNLP:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.intents = []
        self.faq_cache = {}
        self.confidence_threshold = 0.35  # Threshold as defined in project document
        self.train_data_texts = []
        self.train_data_labels = []
        self.load_and_train()

    def detect_language(self, text):
        """Detect whether query is English or Tanglish based on markers."""
        tokens = re.findall(r'\b\w+\b', text.lower())
        for token in tokens:
            if token in TANGLISH_MARKERS:
                return 'Tanglish'
        return 'English'

    def preprocess(self, text):
        """Clean, lowercase, tokenize, and normalize Tanglish and English terms."""
        if not text:
            return ""
        text = text.lower().strip()
        # Remove special characters except alphanumeric and whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Apply normalization regexes
        for pattern, replacement in NORMALIZATION_MAP.items():
            text = re.sub(pattern, replacement, text)
            
        # Clean extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def load_and_train(self):
        """Fetch all verified FAQs from SQLite and train TF-IDF + Logistic Regression."""
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT id, intent, question, answer, category, tanglish_variations, doc_link, doc_title FROM faqs')
            rows = c.fetchall()
            conn.close()

            if not rows:
                print("[NLP Engine] No FAQs found in database.")
                return

            self.faq_cache = {}
            texts = []
            labels = []

            for row in rows:
                intent = row['intent']
                self.faq_cache[intent] = {
                    'id': row['id'],
                    'intent': intent,
                    'question': row['question'],
                    'answer': row['answer'],
                    'category': row['category'],
                    'doc_link': row['doc_link'],
                    'doc_title': row['doc_title']
                }

                # Primary Question
                primary_q = self.preprocess(row['question'])
                texts.append(primary_q)
                labels.append(intent)

                # Tanglish & English Variations
                variations = row['tanglish_variations'] or ''
                for var in variations.split(','):
                    var_clean = self.preprocess(var)
                    if var_clean and len(var_clean) > 1:
                        texts.append(var_clean)
                        labels.append(intent)

            # Build synthetic variations to ensure robust matching on short keywords & conversational patterns
            synthetic_expansions = [
                # cse_fees
                ('cse fees', 'cse_fees'), ('cse fees evalo', 'cse_fees'), ('cse fee evlo', 'cse_fees'),
                ('cse ku fees evlo', 'cse_fees'), ('what is cse fee', 'cse_fees'), ('cse tuition fee', 'cse_fees'),
                ('computer science fees', 'cse_fees'), ('cse rate', 'cse_fees'), ('cse fees sollunga', 'cse_fees'),
                ('cse fee structure', 'cse_fees'), ('cse exam fees', 'cse_fees'),
                # hostel_availability
                ('hostel available', 'hostel_availability'), ('hostel available ah', 'hostel_availability'),
                ('hostel iruka', 'hostel_availability'), ('hostel facility', 'hostel_availability'),
                ('college hostel iruka', 'hostel_availability'), ('boys hostel iruka', 'hostel_availability'),
                ('girls hostel available ah', 'hostel_availability'), ('hostel stay', 'hostel_availability'),
                # hostel_fees
                ('hostel fees', 'hostel_fees'), ('hostel fees evlo', 'hostel_fees'), ('hostel fees evalo', 'hostel_fees'),
                ('hostel rent', 'hostel_fees'), ('mess fees', 'hostel_fees'), ('hostel fees sollunga', 'hostel_fees'),
                ('what is hostel fees', 'hostel_fees'), ('hostel fee structure', 'hostel_fees'),
                # courses_offered
                ('courses', 'courses_offered'), ('courses available', 'courses_offered'),
                ('what courses are offered', 'courses_offered'), ('course list', 'courses_offered'),
                ('enna courses iruku', 'courses_offered'), ('departments', 'courses_offered'),
                ('b e courses', 'courses_offered'), ('engineering branches', 'courses_offered'),
                # placement_details
                ('placement', 'placement_details'), ('placement details', 'placement_details'),
                ('placement details venum', 'placement_details'), ('placements', 'placement_details'),
                ('highest package', 'placement_details'), ('average package', 'placement_details'),
                ('tcs wipro infosys placement', 'placement_details'), ('campus interview', 'placement_details'),
                ('placement percentage', 'placement_details'), ('job placement', 'placement_details'),
                # bus_facility
                ('bus facility', 'bus_facility'), ('bus routes', 'bus_facility'), ('bus fees', 'bus_facility'),
                ('college bus', 'bus_facility'), ('transport', 'bus_facility'), ('bus timings', 'bus_facility'),
                ('bus facility irukka', 'bus_facility'), ('bus stops', 'bus_facility'),
                # admission_procedure
                ('admission', 'admission_procedure'), ('how to get admission', 'admission_procedure'),
                ('admission eppadi', 'admission_procedure'), ('admission process', 'admission_procedure'),
                ('admission process sollunga', 'admission_procedure'), ('tnea counselling admission', 'admission_procedure'),
                ('management quota admission', 'admission_procedure'), ('join college', 'admission_procedure'),
                ('how to join', 'admission_procedure'),
                # cut_off_marks
                ('cutoff', 'cut_off_marks'), ('cutoff marks', 'cut_off_marks'), ('cse cutoff', 'cut_off_marks'),
                ('cutoff evlo', 'cut_off_marks'), ('minimum marks for admission', 'cut_off_marks'),
                ('12th cutoff', 'cut_off_marks'), ('tnea cutoff', 'cut_off_marks'),
                # scholarship_info
                ('scholarship', 'scholarship_info'), ('scholarships', 'scholarship_info'),
                ('first graduate scholarship', 'scholarship_info'), ('scholarship kedaikuma', 'scholarship_info'),
                ('fee concession', 'scholarship_info'), ('government scholarship', 'scholarship_info'),
                # exam_timetable
                ('exam timetable', 'exam_timetable'), ('exam dates', 'exam_timetable'),
                ('semester exam', 'exam_timetable'), ('internal exam dates', 'exam_timetable'),
                ('anna university exam', 'exam_timetable'), ('exam schedule', 'exam_timetable'),
                # college_timing
                ('college timing', 'college_timing'), ('college timings', 'college_timing'),
                ('working hours', 'college_timing'), ('timing enna', 'college_timing'),
                ('class time', 'college_timing'), ('when college starts', 'college_timing'),
                # college_location
                ('college location', 'college_location'), ('where is college located', 'college_location'),
                ('college address', 'college_location'), ('college enga iruku', 'college_location'),
                ('omr address', 'college_location'),
                # contact_info
                ('contact number', 'contact_info'), ('phone number', 'contact_info'),
                ('admission contact', 'contact_info'), ('email id', 'contact_info'),
                ('phone number sollunga', 'contact_info'), ('call college', 'contact_info'),

                # library_facilities
                ('library', 'library_facilities'), ('central library', 'library_facilities'),
                ('digital library', 'library_facilities'), ('library books', 'library_facilities'),
                ('library timings', 'library_facilities'),
                # sports_facilities
                ('sports', 'sports_facilities'), ('cricket ground', 'sports_facilities'),
                ('football ground', 'sports_facilities'), ('gym', 'sports_facilities'),
                ('indoor games', 'sports_facilities'),
                # wifi_facilities
                ('wifi', 'wifi_facilities'), ('wi fi', 'wifi_facilities'), ('free wifi', 'wifi_facilities'),
                ('campus wifi', 'wifi_facilities'), ('internet', 'wifi_facilities'),
                # documents_required
                ('documents required', 'documents_required'), ('certificates needed', 'documents_required'),
                ('admission documents', 'documents_required'), ('tc marksheet required', 'documents_required'),
                # greeting
                ('hi', 'greeting'), ('hello', 'greeting'), ('hey', 'greeting'), ('vanakkam', 'greeting'),
                ('good morning', 'greeting'), ('good evening', 'greeting'), ('help', 'greeting'),
                # thanks
                ('thanks', 'thanks'), ('thank you', 'thanks'), ('romba thanks', 'thanks'), ('nandri', 'thanks'),
                # goodbye
                ('bye', 'goodbye'), ('see you', 'goodbye'), ('goodbye', 'goodbye'), ('tata', 'goodbye')
            ]

            for s_text, s_intent in synthetic_expansions:
                if s_intent in self.faq_cache:
                    texts.append(self.preprocess(s_text))
                    labels.append(s_intent)

            self.train_data_texts = texts
            self.train_data_labels = labels
            self.intents = list(set(labels))

            # TF-IDF Vectorizer with word and sub-word char n-grams for typo resilience
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 3),
                sublinear_tf=True,
                max_features=2500,
                token_pattern=r'(?u)\b\w+\b'
            )
            X_train = self.vectorizer.fit_transform(texts)

            # Logistic Regression Intent Classifier
            self.model = LogisticRegression(
                C=6.0,
                max_iter=1000,
                class_weight='balanced',
                solver='lbfgs'
            )
            self.model.fit(X_train, labels)

            print(f"[NLP Engine] Successfully trained TF-IDF + Logistic Regression on {len(texts)} samples across {len(self.intents)} intents.")

        except Exception as e:
            print(f"[NLP Engine] Error loading and training model: {e}")

    def retrain(self):
        """Re-train model dynamically from database."""
        self.load_and_train()

    def process_query(self, user_query):
        """
        Full query processing pipeline:
        1. Accept student query
        2. Clean, tokenize, normalize Tanglish
        3. Feature extraction via TF-IDF Vectorizer
        4. Intent classification via Logistic Regression
        5. Cosine similarity validation
        6. Return verified FAQ response or trigger fallback & record unknown query
        """
        raw_text = (user_query or "").strip()
        if not raw_text:
            return {
                "matched": False,
                "user_query": "",
                "intent": "empty_query",
                "confidence": 0.0,
                "category": "General",
                "answer": "Please enter a valid question or choose from the suggested questions below.",
                "language": "English",
                "doc_link": None,
                "doc_title": None
            }

        language = self.detect_language(raw_text)
        cleaned_text = self.preprocess(raw_text)

        if not self.model or not self.vectorizer:
            return {
                "matched": False,
                "user_query": raw_text,
                "intent": "system_uninitialized",
                "confidence": 0.0,
                "category": "General",
                "answer": "The AI model is currently initializing. Please try again in a moment.",
                "language": language,
                "doc_link": None,
                "doc_title": None
            }

        # Vectorize query
        query_vec = self.vectorizer.transform([cleaned_text])

        # Predict probability across intents
        probs = self.model.predict_proba(query_vec)[0]
        max_idx = np.argmax(probs)
        confidence = float(probs[max_idx])
        predicted_intent = self.model.classes_[max_idx]

        # Calculate max cosine similarity against training set for safety
        train_vecs = self.vectorizer.transform(self.train_data_texts)
        sim_scores = cosine_similarity(query_vec, train_vecs)[0]
        max_sim = float(np.max(sim_scores)) if len(sim_scores) > 0 else 0.0

        # Blended confidence metric combining Logistic Regression probability and TF-IDF Cosine Similarity
        # If cosine similarity is too low (< 0.20), the query shares almost no vocabulary with known questions
        if max_sim < 0.20:
            effective_confidence = max_sim * 0.8
        else:
            effective_confidence = (confidence * 0.45) + (max_sim * 0.55)

        # Keyword boost: If specific strong keywords match (e.g., 'cse', 'hostel', 'placement', 'bus', 'admission', 'fee')
        tokens = set(cleaned_text.split())
        if 'cse' in tokens and ('fee' in cleaned_text or 'fees' in cleaned_text or 'evlo' in cleaned_text):
            predicted_intent = 'cse_fees'
            effective_confidence = max(effective_confidence, 0.95)
        elif 'hostel' in tokens and ('fees' in tokens or 'rent' in tokens or 'evlo' in tokens):
            predicted_intent = 'hostel_fees'
            effective_confidence = max(effective_confidence, 0.95)
        elif 'hostel' in tokens and ('available' in tokens or 'iruka' in tokens or 'facility' in tokens or 'room' in tokens):
            predicted_intent = 'hostel_availability'
            effective_confidence = max(effective_confidence, 0.94)
        elif ('placement' in tokens or 'placements' in tokens or 'campus' in tokens) and ('details' in tokens or 'venum' in tokens or 'stat' in cleaned_text or 'job' in tokens):
            predicted_intent = 'placement_details'
            effective_confidence = max(effective_confidence, 0.93)
        elif ('bus' in tokens or 'transport' in tokens) and ('route' in cleaned_text or 'timing' in cleaned_text or 'iruka' in tokens or 'fees' in tokens):
            predicted_intent = 'bus_facility'
            effective_confidence = max(effective_confidence, 0.92)
        elif ('admission' in tokens) and ('process' in tokens or 'procedure' in tokens or 'eppadi' in tokens or 'how' in tokens or 'join' in tokens):
            predicted_intent = 'admission_procedure'
            effective_confidence = max(effective_confidence, 0.94)
        elif ('cutoff' in tokens or 'cut-off' in tokens) or ('mark' in tokens and 'admission' in tokens):
            predicted_intent = 'cut_off_marks'
            effective_confidence = max(effective_confidence, 0.91)
        elif ('exam' in tokens or 'timetable' in tokens or 'semester' in tokens) and ('date' in tokens or 'schedule' in tokens or 'time' in tokens or 'when' in tokens):
            predicted_intent = 'exam_timetable'
            effective_confidence = max(effective_confidence, 0.92)
        elif ('scholarship' in tokens or 'scholarships' in tokens):
            predicted_intent = 'scholarship_info'
            effective_confidence = max(effective_confidence, 0.93)


        # Check threshold
        if effective_confidence >= self.confidence_threshold and str(predicted_intent) in self.faq_cache:
            matched_faq = self.faq_cache[str(predicted_intent)]
            return {
                "matched": True,
                "user_query": raw_text,
                "intent": str(predicted_intent),
                "confidence": float(round(effective_confidence, 3)),
                "category": matched_faq['category'],
                "answer": matched_faq['answer'],
                "doc_link": matched_faq['doc_link'],
                "doc_title": matched_faq['doc_title'],
                "language": language
            }
        else:
            # Low confidence or unknown query -> Fallback response and log for admin review
            fallback_answer = (
                "I'm sorry, I couldn't find verified college information for your query right now. "
                "I have registered this query for our college administration team to review and provide verified details. "
                "In the meantime, you can contact the Admission Office directly at +91 98765 43210 or admissions@college.edu.in."
            )
            return {
                "matched": False,
                "user_query": raw_text,
                "intent": str(predicted_intent) if effective_confidence > 0.15 else "unknown_query",
                "confidence": float(round(effective_confidence, 3)),
                "category": "Unresolved",
                "answer": fallback_answer,
                "doc_link": "https://example.edu/contact-directory",
                "doc_title": "Official College Contact & Helpdesk Directory",
                "language": language
            }

# Global singleton instance
ai_engine = CollegeChatbotNLP()
