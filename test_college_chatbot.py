"""
Automated End-to-End Test Suite for College Chatbot Using AI.
Tests:
- Database connectivity & tables
- TF-IDF + Logistic Regression Intent Classification
- English and Tanglish queries
- Low-confidence unknown query fallback
- Dynamic FAQ insertion & automatic model retraining
- Admin authentication
"""

import os
import sys
import unittest
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from database import init_db, get_db_connection, DB_PATH
from nlp_engine import ai_engine
from app import app

class CollegeChatbotTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reset DB cleanly before running tests
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        ai_engine.retrain()
        cls.client = app.test_client()

    def test_01_database_tables(self):
        """Verify SQLite tables exist and have records."""
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in c.fetchall()]
        self.assertIn('faqs', tables)
        self.assertIn('admin', tables)
        self.assertIn('unknown_queries', tables)
        self.assertIn('chat_history', tables)
        self.assertIn('college_settings', tables)

        c.execute("SELECT COUNT(*) FROM faqs")
        faq_count = c.fetchone()[0]
        self.assertGreater(faq_count, 15, "Knowledge base should have more than 15 seed FAQs.")
        conn.close()

    def test_02_nlp_english_and_tanglish_queries(self):
        """Verify TF-IDF + Logistic Regression identifies intents across English and Tanglish."""
        test_queries = [
            ("CSE ku fees evlo?", "cse_fees", "Tanglish"),
            ("What is CSE fees?", "cse_fees", "English"),
            ("Hostel available ah?", "hostel_availability", "Tanglish"),
            ("Is hostel facility available?", "hostel_availability", "English"),
            ("How to get admission?", "admission_procedure", "English"),
            ("Admission eppadi?", "admission_procedure", "Tanglish"),
            ("Placement details venum", "placement_details", "Tanglish"),
            ("Is bus facility available?", "bus_facility", "English"),
            ("When is the exam timetable released?", "exam_timetable", "English"),
        ]

        for query, expected_intent, expected_lang in test_queries:
            result = ai_engine.process_query(query)
            self.assertTrue(result['matched'], f"Query '{query}' should match an intent.")
            self.assertEqual(result['intent'], expected_intent, f"Query '{query}' predicted {result['intent']}, expected {expected_intent}")
            self.assertGreaterEqual(result['confidence'], 0.35, f"Confidence for '{query}' should be >= 0.35")
            print(f"[PASS] '{query}' -> Intent: {result['intent']} (Conf: {result['confidence']:.2f}, Lang: {result['language']})")

    def test_03_unknown_query_fallback(self):
        """Verify unknown or out-of-domain queries trigger fallback."""
        query = "What about canteen menu?"
        result = ai_engine.process_query(query)
        self.assertFalse(result['matched'], f"Query '{query}' should be unknown initially.")
        self.assertIn("couldn't find verified college information", result['answer'])
        print(f"[PASS] Unknown query '{query}' correctly triggered fallback response.")

    def test_04_api_chat_endpoint(self):
        """Verify /api/chat HTTP endpoint returns structured JSON."""
        response = self.client.post('/api/chat', json={'query': 'CSE ku fees evlo?'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['intent'], 'cse_fees')
        self.assertIn('75,000', data['answer'])

    def test_05_admin_login_auth(self):
        """Verify admin login authenticates valid credentials and rejects invalid ones."""
        # 1. Invalid login
        res_bad = self.client.post('/admin/login', data={'username': 'admin', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', res_bad.data)

        # 2. Valid login
        res = self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertIn(b'Dashboard Overview', res.data)

        # 3. Logout
        self.client.get('/admin/logout')

    def test_06_dynamic_faq_addition_and_retraining(self):
        """Verify demo flow: Unknown query -> Admin adds FAQ -> Model retrains -> Chatbot answers!"""
        # 1. Ask unknown question
        unknown_q = "Is there a college canteen menu?"
        res1 = ai_engine.process_query(unknown_q)
        self.assertFalse(res1['matched'], "Should initially be unmatched.")

        # 2. Simulate Admin adding the FAQ to SQLite
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO faqs (intent, question, answer, category, tanglish_variations, doc_link, doc_title)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'canteen_menu_intent',
            'Is there a college canteen menu?',
            'Yes, our cafeteria provides freshly prepared vegetarian and non-vegetarian meals, fresh juices, and snacks from 8:00 AM to 5:30 PM.',
            'Campus Facilities',
            'canteen menu enna?, canteen food eppadi?, mess rate evlo?',
            'https://example.edu/canteen.pdf',
            'Canteen Menu Document'
        ))
        conn.commit()
        conn.close()

        # 3. Trigger retrain
        ai_engine.retrain()

        # 4. Ask the same question again
        res2 = ai_engine.process_query(unknown_q)
        self.assertTrue(res2['matched'], "Should now match after dynamic retraining!")
        self.assertEqual(res2['intent'], 'canteen_menu_intent')
        self.assertIn('freshly prepared vegetarian', res2['answer'])
        print(f"[PASS] Dynamic Retraining Verified: '{unknown_q}' now answered with {res2['confidence']:.2f} confidence!")

if __name__ == '__main__':
    unittest.main()
