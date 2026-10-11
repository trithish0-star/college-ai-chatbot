"""
Database module for College Chatbot Using AI.
Handles SQLite database connection, table creation, seed data initialization,
and database queries for FAQs, Admin credentials, Unknown Queries, Chat History,
and College Information.
"""

import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'college.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # 1. FAQ Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intent TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL,
            tanglish_variations TEXT,
            doc_link TEXT,
            doc_title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Admin Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'Administrator',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Unknown Queries Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS unknown_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            predicted_intent TEXT,
            confidence REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Pending Review',
            admin_answer TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Chat History Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            intent TEXT,
            confidence REAL DEFAULT 0.0,
            category TEXT,
            language TEXT DEFAULT 'English',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. College Settings Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS college_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')

    conn.commit()

    # Seed Admin User if not exists
    c.execute('SELECT COUNT(*) FROM admin')
    if c.fetchone()[0] == 0:
        default_admin_hash = generate_password_hash('admin123')
        c.execute('''
            INSERT INTO admin (username, password_hash, email, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', default_admin_hash, 'admin@college.edu.in', 'Chief Administrator'))
        conn.commit()

    # Seed Settings if empty
    settings_data = {
        'college_name': 'Anna Adarsh Institute of Technology & Science',
        'college_code': 'C-1428',
        'tagline': 'Empowering Minds, Innovating Futures — Affiliated to Anna University & Approved by AICTE',
        'phone': '+91 98765 43210 / 044-24567890',
        'email': 'admissions@college.edu.in',
        'address': 'Kamaraj Nagar, IT Highway (OMR), Chennai, Tamil Nadu - 600119',
        'office_hours': 'Monday to Saturday: 8:30 AM – 5:00 PM',
        'tnea_counselling_code': '3462',
        'admission_status': 'Admissions Open for Academic Year 2026-27'
    }
    for k, v in settings_data.items():
        c.execute('INSERT OR IGNORE INTO college_settings (key, value) VALUES (?, ?)', (k, v))
    conn.commit()

    # Seed Default Verified FAQs (Covering 25 distinct intents from project document)
    c.execute('SELECT COUNT(*) FROM faqs')
    if c.fetchone()[0] == 0:
        initial_faqs = [
            (
                "cse_fees",
                "What is CSE fees?",
                "Computer Science and Engineering (CSE) tuition fee is ₹75,000 per academic year. Exam fees and laboratory maintenance are ₹7,500 per semester. Total annual academic fee is approx ₹82,500.",
                "Fees",
                "CSE ku fees evlo?, cse fees evalo?, how much is cse fees?, cse fee details sollunga, computer science fees evlo, cse course fees",
                "/document/cse-fees",
                "CSE Fee Structure Official Document (PDF)"
            ),
            (
                "hostel_availability",
                "Hostel available?",
                "Yes, we provide separate secured hostel facilities for boys and girls on campus. Facilities include 24/7 Wi-Fi, hygienic south/north Indian mess, mineral water RO plant, gym, medical room, and 24/7 CCTV security.",
                "Hostel",
                "hostel irukka?, hostel iruka, hostel facility available ah?, hostel room details, boys hostel girls hostel available ah?, college hostel iruka",
                "/document/hostel-guide",
                "Hostel Rules & Room Types Booklet"
            ),
            (
                "hostel_fees",
                "What is hostel fees?",
                "Hostel fee is ₹60,000 per year which includes 3-sharing/4-sharing furnished room accommodation, electricity, laundry access, and 3-times hygienic buffet meals with evening snacks.",
                "Hostel",
                "hostel fees evlo?, hostel ku fees evalo?, hostel rent evlo?, mess fees evlo?, hostel fee details sollunga",
                "/document/hostel-guide",
                "Hostel Fee Breakdown & Challan"
            ),
            (
                "courses_offered",
                "What courses are offered?",
                "We offer B.E. programs in CSE, AI & Data Science (AI&DS), ECE, Mechanical, and Civil Engineering. At the postgraduate level, we offer M.E. CSE, Embedded Systems, and MBA. All courses are AICTE approved and Anna University affiliated.",
                "Courses",
                "courses available, what are the courses offered?, enna enna courses iruku?, course list sollunga, enna group iruku?, ug courses pg courses",
                "/document/admission-portal",
                "Complete Course Catalog & Syllabus"
            ),
            (
                "college_timing",
                "What is the college timing?",
                "College academic working hours are from 9:00 AM to 4:00 PM, Monday through Friday. On working Saturdays, classes or lab practicals operate until 1:00 PM. Administrative office functions from 8:30 AM to 5:00 PM.",
                "Admissions",
                "college timing enna?, college timings, class time enna?, working hours sollunga, what time does college start and close?",
                "/document/exam-schedule",
                "Official Academic Working Hours Schedule"
            ),
            (
                "placement_details",
                "What are the placement details?",
                "Our college maintains an outstanding 85%+ placement record! Top recruiting companies include TCS, Infosys, Wipro, Cognizant, Zoho, HCL, and Accenture. The highest package offered is ₹14.5 LPA and average package is ₹5.2 LPA.",
                "Placements",
                "placement eppadi iruku?, placement details venum, campus interview varuma?, top companies placement, placement percentage evlo?, job guarantee iruka?",
                "/document/placement-report",
                "Latest Campus Placement & Recruiter Report"
            ),
            (
                "bus_facility",
                "Is bus facility available?",
                "Yes, 35+ air-conditioned and standard college buses ply across all major routes covering Chennai, Tambaram, Chengalpattu, Velachery, Avadi, and Kanchipuram. Annual transport fee is ₹12,000 to ₹16,000 depending on stage distance.",
                "Transport",
                "bus facility irukka?, bus fees evlo?, college bus routes enna?, transport facility available ah?, college bus varuma?",
                "/document/bus-routes",
                "College Bus Routes & Pickup Timings"
            ),
            (
                "admission_procedure",
                "How to get admission?",
                "Admissions are conducted through two streams: 1) TNEA Single Window Government Counselling based on 12th standard cut-off marks (Counselling Code: 3462). 2) Management Quota direct admission. Candidates need 10th & 12th marksheets, TC, and community certificate.",
                "Admissions",
                "admission eppadi?, admission process sollunga, admission procedure, how to join college?, join panna enna pannanum?, admission form eppadi apply pandrathu?",
                "/document/admission-portal",
                "Online Admission Application & Guidelines"
            ),
            (
                "college_location",
                "Where is the college located?",
                "The college campus is located at IT Highway (OMR), Kamaraj Nagar, Chennai, Tamil Nadu - 600119. It is conveniently situated 4 km from Sholinganallur junction and 15 km from Tambaram Railway Station.",
                "Campus Facilities",
                "where is college located?, college enga iruku?, college address enna?, campus location sollunga, landmark enna?",
                "/document/admission-portal",
                "Google Maps Live Campus Location"
            ),
            (
                "contact_info",
                "What is the contact number and email?",
                "You can reach our Admission Cell at +91 98765 43210 or 044-24567890. Email us at admissions@college.edu.in or principal@college.edu.in. Office is open Mon-Sat 8:30 AM to 5:00 PM.",
                "Admissions",
                "contact number?, phone number sollunga, college email id enna?, principal contact number, admission cell phone number",
                "/document/admission-portal",
                "College Official Contact Directory"
            ),
            (
                "scholarship_info",
                "Are scholarships available?",
                "Yes! We offer Government First Graduate Scholarships (₹25,000 tuition waiver), SC/ST Post-Matric scholarships, 7.5% Govt School reservation free education, and Merit Scholarships (up to 50% tuition waiver for >90% in 12th Board).",
                "Fees",
                "scholarship kedaikuma?, scholarship details sollunga, first graduate scholarship iruka?, fee concession kedaikuma?, merit scholarship evlo?",
                "/document/cse-fees",
                "Scholarship Scheme Eligibility & Form"
            ),
            (
                "exam_timetable",
                "When is the exam timetable released?",
                "Anna University Semester Examinations timetable is published 3 weeks before exams on the college notice board and online student portal. Odd semester exams typically start in November/December and Even semester exams in April/May.",
                "Examinations",
                "exam timetable eppo varum?, semester exam dates enna?, exam schedule sollunga, internal exam timetable, anna university exam dates",
                "/document/exam-schedule",
                "Semester Examination Schedule & Rules"
            ),
            (
                "cut_off_marks",
                "What is the required cut-off for CSE?",
                "For CSE, the expected cut-off marks in TNEA counselling are: OC (175+), BC (165+), MBC (155+), and SC/ST (140+). Management quota admissions are based on minimum 60% aggregate in Physics, Chemistry, and Mathematics.",
                "Admissions",
                "cutoff evlo venum?, cse cutoff marks evlo?, minimum marks required for admission?, 12th cutoff evlo irukanum?, eligibility marks enna?",
                "/document/admission-portal",
                "Previous Year TNEA Cut-Off Trends"
            ),
            (
                "library_facilities",
                "What are the library facilities?",
                "Our Central Digital Library houses over 45,000 volumes, 120 national/international journals, IEEE/ScienceDirect e-resources, DELNET access, a 100-seat digital reference section, and reprographic facilities. Open 8:00 AM to 7:00 PM.",
                "Campus Facilities",
                "library irukka?, library timing enna?, books borrow panna mudiyuma?, digital library access iruka?, library details sollunga",
                "/document/hostel-guide",
                "Central Digital Library Catalog Portal"
            ),
            (
                "sports_facilities",
                "What sports facilities are available?",
                "We provide extensive sports infrastructure including cricket ground with turf nets, FIFA-standard football ground, basketball court with floodlights, volleyball courts, badminton indoor stadium, gym, and table tennis.",
                "Campus Facilities",
                "sports facilities irukka?, cricket football ground iruka?, gym facility available ah?, indoor games iruka?, sports quota admission iruka?",
                "/document/hostel-guide",
                "Sports Facilities & Tournaments Guide"
            ),
            (
                "wifi_facilities",
                "Is Wi-Fi available across campus?",
                "Yes, high-speed 1 Gbps fiber optic Wi-Fi connectivity is available across all academic blocks, digital classrooms, central library, and student hostels for authorized student laptops and devices.",
                "Campus Facilities",
                "wifi campus ah?, wifi speed evlo?, free wifi kedaikuma?, internet connection hostel la iruka?, wifi password eppadi vaangarathu?",
                "/document/hostel-guide",
                "Campus IT & Wi-Fi Usage Policy"
            ),
            (
                "internship_opportunities",
                "Are internship opportunities provided?",
                "Yes, our Corporate Relations & Placement Cell arranges mandatory 4th-year paid internships and 2nd/3rd-year summer internships with leading tech companies, startups, and R&D centers with stipends up to ₹25,000/month.",
                "Placements",
                "internship kedaikuma?, internship stipend evlo?, company internship provide pannuvangala?, training and internship details",
                "/document/placement-report",
                "Internship Industry Partners List"
            ),
            (
                "dress_code",
                "What is the college dress code?",
                "Students must adhere to a formal, decent dress code. Boys: Formal shirts, trousers with shoes. Girls: Chudidar with dupatta or formal formal attire. Laboratory coats are mandatory during chemistry, mechanical, and physics practicals.",
                "Admissions",
                "dress code irukka?, uniform iruka?, casual dress allow pannuvangala?, lab coat compulsory ah?, dress rules enna?",
                "/document/admission-portal",
                "Student Code of Conduct & Dress Regulations"
            ),
            (
                "documents_required",
                "What documents are required for admission?",
                "Documents required: 1) 10th & 12th Original Marksheets, 2) Transfer Certificate (TC) & Conduct Certificate, 3) Community Certificate, 4) TNEA Counselling Allotment Order (if applicable), 5) Aadhaar Card copy, 6) 6 Passport size photos, 7) First Graduate Certificate (if applicable).",
                "Admissions",
                "admission ku enna documents venum?, required certificates for admission, original certificates submit pannanuma?, TC and marksheet venuma?",
                "/document/admission-portal",
                "Admission Document Verification Checklist"
            ),
            (
                "ece_fees",
                "What is ECE fees?",
                "Electronics and Communication Engineering (ECE) tuition fee is ₹70,000 per academic year. Lab and examination charges total approx ₹7,000 per semester.",
                "Fees",
                "ece fees evlo?, ece course fee evalo?, electronics department fees sollunga",
                "/document/cse-fees",
                "Engineering Department Fees Chart"
            ),
            (
                "mba_fees",
                "What is MBA fees and course details?",
                "Our two-year Master of Business Administration (MBA) program fee is ₹65,000 per year. Specializations include Finance, Marketing, HR, Business Analytics, and Operations.",
                "Fees",
                "mba fees evlo?, mba course details sollunga, master of business administration fee, pg course fees",
                "/document/cse-fees",
                "MBA Program Brochure & Fee Structure"
            ),
            (
                "greeting",
                "Hello / Hi",
                "Hello! 👋 Welcome to your College Assistant. How can I help you today? You can ask me anything about admissions, courses, fees, hostel, bus transport, exams, or placements in English or Tanglish!",
                "General",
                "hi, hello, vanakkam, good morning, good afternoon, namaste, hey there, ai bot",
                "/document/admission-portal",
                "College Overview & Virtual Tour"
            ),
            (
                "thanks",
                "Thank you",
                "You're very welcome! 😊 Feel free to ask if you have any more doubts regarding admissions, fees, hostel, or exams. Best wishes for your academic journey!",
                "General",
                "thanks, thank you so much, romba thanks, nandri, ok thanks, bye thanks",
                "/document/admission-portal",
                "Contact Enquiry Cell"
            ),
            (
                "goodbye",
                "Bye / See you",
                "Goodbye! Have a great day ahead! 👋 Feel free to chat again anytime you need college information.",
                "General",
                "bye, tata, see you, goodbye, bye bye, கிளம்புறேன்",
                "/",
                "College Official Portal"
            )
        ]
        c.executemany('''
            INSERT INTO faqs (intent, question, answer, category, tanglish_variations, doc_link, doc_title)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', initial_faqs)
        conn.commit()

    # Seed Sample Unknown Queries for Admin Demo
    c.execute('SELECT COUNT(*) FROM unknown_queries')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO unknown_queries (query_text, predicted_intent, confidence, status, admin_answer)
            VALUES (?, ?, ?, ?, ?)
        ''', ('What about canteen menu?', 'canteen_facilities', 0.32, 'Pending Review', None))
        c.execute('''
            INSERT INTO unknown_queries (query_text, predicted_intent, confidence, status, admin_answer)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Is swimming pool facility available inside campus?', 'sports_facilities', 0.28, 'Pending Review', None))
        conn.commit()

    # Seed Sample Chat History for Analytics
    c.execute('SELECT COUNT(*) FROM chat_history')
    if c.fetchone()[0] == 0:
        sample_chats = [
            ('demo_sess_1', 'CSE ku fees evlo?', 'Computer Science and Engineering (CSE) tuition fee is ₹75,000 per academic year...', 'cse_fees', 0.94, 'Fees', 'Tanglish'),
            ('demo_sess_1', 'Hostel available ah?', 'Yes, we provide separate secured hostel facilities for boys and girls on campus...', 'hostel_availability', 0.91, 'Hostel', 'Tanglish'),
            ('demo_sess_2', 'How to get admission?', 'Admissions are conducted through two streams: 1) TNEA Single Window Government Counselling...', 'admission_procedure', 0.88, 'Admissions', 'English'),
            ('demo_sess_2', 'Placement details venum', 'Our college maintains an outstanding 85%+ placement record! Top recruiting companies...', 'placement_details', 0.93, 'Placements', 'Tanglish'),
            ('demo_sess_3', 'Bus facility available?', 'Yes, 35+ air-conditioned and standard college buses ply across all major routes...', 'bus_facility', 0.89, 'Transport', 'English'),
            ('demo_sess_3', 'What is hostel fees?', 'Hostel fee is ₹60,000 per year which includes 3-sharing/4-sharing furnished room accommodation...', 'hostel_fees', 0.95, 'Hostel', 'English'),
            ('demo_sess_4', 'What courses are offered?', 'We offer B.E. programs in CSE, AI & Data Science (AI&DS), ECE, Mechanical, and Civil Engineering...', 'courses_offered', 0.92, 'Courses', 'English'),
            ('demo_sess_5', 'When is the exam timetable?', 'Anna University Semester Examinations timetable is published 3 weeks before exams...', 'exam_timetable', 0.87, 'Examinations', 'English'),
        ]
        c.executemany('''
            INSERT INTO chat_history (session_id, user_query, bot_response, intent, confidence, category, language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_chats)
        conn.commit()

    conn.close()
    print("[Database] Initialized SQLite schema and seed records successfully.")

if __name__ == '__main__':
    init_db()
