"""
Flask Application for College Chatbot Using AI.
Provides:
- Student-facing Homepage with comprehensive college information hub
- Dedicated Figma-inspired AI Chatbot Interface (/chat)
- Interactive Floating Chatbot Widget on all pages
- Real-time Query Processing API with TF-IDF + Logistic Regression
- Secure Admin Authentication & Session Management
- Comprehensive Admin Dashboard with FAQ CRUD, Unknown Queries review, and Live Analytics
"""

import os
import sys
import json
import sqlite3
import uuid
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, jsonify, session,
    redirect, url_for, flash
)
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db_connection, init_db, DB_PATH
from nlp_engine import ai_engine
from documents_data import get_document_by_slug, COLLEGE_DOCUMENTS

# Force UTF-8 standard output for terminal logging on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'college_ai_chatbot_secure_key_2026_x89f')

# Ensure database is created on startup
if not os.path.exists(DB_PATH):
    init_db()

# ==========================================
# HELPER DECORATORS & FUNCTIONS
# ==========================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            flash('Please log in with administrator credentials to access this page.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_college_settings():
    """Retrieve college configuration key-values from database."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT key, value FROM college_settings')
        rows = c.fetchall()
        conn.close()
        return {r['key']: r['value'] for r in rows}
    except Exception as e:
        return {
            'college_name': 'Anna Adarsh Institute of Technology & Science',
            'tagline': 'Empowering Minds, Innovating Futures — Affiliated to Anna University & AICTE Approved',
            'phone': '+91 98765 43210',
            'email': 'admissions@college.edu.in',
            'address': 'OMR, Chennai, Tamil Nadu',
            'admission_status': 'Admissions Open 2026-27'
        }

@app.context_processor
def inject_global_data():
    """Inject college settings into all Jinja templates."""
    return {'settings': get_college_settings()}

# ==========================================
# PUBLIC ROUTES
# ==========================================

@app.route('/')
def index():
    """Public landing page with complete college sections, how it works, tech stack, and floating chatbot."""
    conn = get_db_connection()
    c = conn.cursor()
    # Fetch categorized FAQs to display in college information cards
    c.execute('SELECT * FROM faqs ORDER BY category, id')
    faqs = c.fetchall()
    
    # Group faqs by category for easy section rendering
    categorized_faqs = {}
    for faq in faqs:
        cat = faq['category']
        if cat not in categorized_faqs:
            categorized_faqs[cat] = []
        categorized_faqs[cat].append(dict(faq))
        
    conn.close()
    return render_template('index.html', categorized_faqs=categorized_faqs)

@app.route('/chat')
def chat():
    """Dedicated Figma-inspired AI Chatbot workspace matching the project design."""
    return render_template('chat.html')

@app.route('/document/<doc_slug>')
def view_document(doc_slug):
    """View official verified college document on branded letterhead."""
    doc = get_document_by_slug(doc_slug)
    return render_template('document_viewer.html', doc=doc)

@app.route('/api/document/<doc_slug>')
def api_get_document(doc_slug):
    """Return JSON representation of document for in-page modal preview."""
    doc = get_document_by_slug(doc_slug)
    return jsonify({'success': True, 'document': doc})

# ==========================================
# CHATBOT API ENDPOINTS
# ==========================================

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    Main Chatbot query processing endpoint:
    1. Parse student query
    2. Run NLP Preprocessing, TF-IDF Vectorization, and Logistic Regression
    3. Retrieve verified answer from SQLite
    4. Save to chat_history or unknown_queries
    5. Return JSON payload
    """
    data = request.get_json(force=True, silent=True) or {}
    user_query = data.get('query', '').strip()
    session_id = data.get('session_id') or session.get('chat_session_id')
    
    if not session_id:
        session_id = str(uuid.uuid4())[:8]
        session['chat_session_id'] = session_id

    if not user_query:
        return jsonify({
            'success': False,
            'answer': 'Please enter a query or select from the quick suggestion chips.',
            'category': 'General',
            'confidence': 0.0,
            'matched': False
        }), 400

    # Process via AI engine
    result = ai_engine.process_query(user_query)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Log query to chat_history
    c.execute('''
        INSERT INTO chat_history (session_id, user_query, bot_response, intent, confidence, category, language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        session_id,
        user_query,
        result['answer'],
        result['intent'],
        result['confidence'],
        result['category'],
        result['language']
    ))
    
    # If query was unknown or below confidence threshold, record in unknown_queries
    if not result['matched']:
        c.execute('''
            INSERT INTO unknown_queries (query_text, predicted_intent, confidence, status)
            VALUES (?, ?, ?, 'Pending Review')
        ''', (user_query, result['intent'], result['confidence']))
        
    conn.commit()
    conn.close()

    intent_to_slug = {
        'cse_fees': 'cse-fees',
        'hostel_availability': 'hostel-guide',
        'hostel_fees': 'hostel-guide',
        'placement_details': 'placement-report',
        'internship_opportunities': 'placement-report',
        'bus_facility': 'bus-routes',
        'admission_procedure': 'admission-portal',
        'cut_off_marks': 'admission-portal',
        'documents_required': 'admission-portal',
        'courses_offered': 'admission-portal',
        'scholarship_info': 'cse-fees',
        'exam_timetable': 'exam-schedule',
        'college_timing': 'exam-schedule',
        'canteen_facilities': 'canteen-menu',
        'canteen_menu_intent': 'canteen-menu',
    }
    
    intent_name = str(result.get('intent', ''))
    doc_link = result.get('doc_link')
    doc_title = result.get('doc_title')
    
    if intent_name in intent_to_slug:
        slug = intent_to_slug[intent_name]
        doc_link = f"/document/{slug}"
        doc_obj = get_document_by_slug(slug)
        doc_title = doc_obj['title']
    elif not doc_link or 'example.edu' in str(doc_link):
        doc_link = "/document/admission-portal"
        doc_title = "Online Admission Application & Guidelines"

    return jsonify({
        'success': True,
        'user_query': user_query,
        'answer': result['answer'],
        'intent': result['intent'],
        'confidence': result['confidence'],
        'category': result['category'],
        'language': result['language'],
        'matched': result['matched'],
        'doc_link': doc_link,
        'doc_title': doc_title,
        'timestamp': datetime.now().strftime('%I:%M %p')
    })

@app.route('/api/quick-questions', methods=['GET'])
def get_quick_questions():
    """Return default quick prompt suggestions."""
    questions = [
        {"title": "CSE Course Fees", "subtitle": "CSE ku fees evlo?", "query": "CSE ku fees evlo?"},
        {"title": "Hostel Facilities", "subtitle": "Hostel available ah?", "query": "Hostel available ah?"},
        {"title": "Admission Process", "subtitle": "How to get admission?", "query": "How to get admission?"},
        {"title": "Placement Records", "subtitle": "Placement details venum", "query": "Placement details venum"},
        {"title": "Bus & Transport", "subtitle": "College bus routes & fees", "query": "Is bus facility available?"},
        {"title": "Exam Schedule", "subtitle": "When is the exam timetable?", "query": "When is the exam timetable released?"},
        {"title": "Scholarship Details", "subtitle": "Scholarship kedaikuma?", "query": "Are scholarships available?"},
        {"title": "Courses Offered", "subtitle": "What courses are available?", "query": "What courses are offered?"}
    ]
    return jsonify({'success': True, 'questions': questions})

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Retrieve chat history for the active session."""
    session_id = request.args.get('session_id') or session.get('chat_session_id')
    if not session_id:
        return jsonify({'success': True, 'history': []})
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT user_query, bot_response, intent, confidence, category, language, timestamp
        FROM chat_history
        WHERE session_id = ?
        ORDER BY id ASC
    ''', (session_id,))
    rows = c.fetchall()
    conn.close()
    
    history = [dict(r) for r in rows]
    return jsonify({'success': True, 'history': history})

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat():
    """Clear chat session identifier."""
    session['chat_session_id'] = str(uuid.uuid4())[:8]
    return jsonify({'success': True, 'message': 'Chat session cleared.', 'new_session_id': session['chat_session_id']})

# ==========================================
# SECURE ADMIN ROUTES
# ==========================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page with secure password hashing verification."""
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('admin_login.html')

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM admin WHERE username = ? OR email = ?', (username, username))
        admin = c.fetchone()
        conn.close()

        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin['id']
            session['admin_username'] = admin['username']
            session['admin_role'] = admin['role']
            flash(f'Welcome back, {admin["username"]}! Successfully authenticated.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password. Please verify credentials.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Log out admin and clear session."""
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    session.pop('admin_role', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard overview with metrics, quick actions, and recent activity."""
    conn = get_db_connection()
    c = conn.cursor()

    # 1. Total FAQs
    c.execute('SELECT COUNT(*) FROM faqs')
    total_faqs = c.fetchone()[0]

    # 2. Total Queries Received
    c.execute('SELECT COUNT(*) FROM chat_history')
    total_queries = c.fetchone()[0]

    # 3. Unanswered / Pending Unknown Queries
    c.execute("SELECT COUNT(*) FROM unknown_queries WHERE status = 'Pending Review'")
    pending_unknown = c.fetchone()[0]

    # 4. Total Resolved Unknown Queries
    c.execute("SELECT COUNT(*) FROM unknown_queries WHERE status = 'Resolved'")
    resolved_unknown = c.fetchone()[0]

    # 5. Top Categories Count
    c.execute('''
        SELECT category, COUNT(*) as count 
        FROM faqs 
        GROUP BY category 
        ORDER BY count DESC
    ''')
    category_counts = [dict(r) for r in c.fetchall()]

    # 6. Recent Chat Queries
    c.execute('''
        SELECT * FROM chat_history 
        ORDER BY id DESC LIMIT 10
    ''')
    recent_chats = [dict(r) for r in c.fetchall()]

    # 7. Recent Unknown Queries
    c.execute('''
        SELECT * FROM unknown_queries 
        ORDER BY id DESC LIMIT 8
    ''')
    recent_unknown = [dict(r) for r in c.fetchall()]

    # 8. All FAQs for management table
    c.execute('SELECT * FROM faqs ORDER BY id DESC')
    all_faqs = [dict(r) for r in c.fetchall()]

    conn.close()

    metrics = {
        'total_faqs': total_faqs,
        'total_queries': total_queries,
        'pending_unknown': pending_unknown,
        'resolved_unknown': resolved_unknown,
        'resolution_rate': round(((total_queries - pending_unknown) / max(total_queries, 1)) * 100, 1),
        'category_counts': category_counts,
        'recent_chats': recent_chats,
        'recent_unknown': recent_unknown,
        'all_faqs': all_faqs
    }

    return render_template('admin_dashboard.html', metrics=metrics)

@app.route('/admin/faq/add', methods=['POST'])
@login_required
def add_faq():
    """Add new FAQ to database and retrain AI model."""
    question = request.form.get('question', '').strip()
    answer = request.form.get('answer', '').strip()
    category = request.form.get('category', 'General').strip()
    tanglish_variations = request.form.get('tanglish_variations', '').strip()
    doc_link = request.form.get('doc_link', '').strip()
    doc_title = request.form.get('doc_title', '').strip()
    unknown_id = request.form.get('unknown_id')

    if not question or not answer:
        flash('Question and Answer are required fields.', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Generate a clean intent identifier
    intent_slug = question.lower().strip()
    intent_slug = ''.join(c if c.isalnum() else '_' for c in intent_slug)[:30].strip('_')
    if not intent_slug:
        intent_slug = f"custom_intent_{int(datetime.now().timestamp())}"

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO faqs (intent, question, answer, category, tanglish_variations, doc_link, doc_title, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (intent_slug, question, answer, category, tanglish_variations, doc_link, doc_title))

    # If this FAQ was added from an unknown query, mark it resolved
    if unknown_id:
        c.execute('''
            UPDATE unknown_queries 
            SET status = 'Resolved', admin_answer = ? 
            WHERE id = ?
        ''', (answer, unknown_id))

    conn.commit()
    conn.close()

    # Retrain model in-memory immediately!
    ai_engine.retrain()

    flash(f'New FAQ "{question}" added successfully and AI model updated!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/faq/edit/<int:faq_id>', methods=['POST'])
@login_required
def edit_faq(faq_id):
    """Edit existing FAQ record and retrain model."""
    question = request.form.get('question', '').strip()
    answer = request.form.get('answer', '').strip()
    category = request.form.get('category', 'General').strip()
    tanglish_variations = request.form.get('tanglish_variations', '').strip()
    doc_link = request.form.get('doc_link', '').strip()
    doc_title = request.form.get('doc_title', '').strip()

    if not question or not answer:
        flash('Question and Answer cannot be empty.', 'danger')
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE faqs 
        SET question = ?, answer = ?, category = ?, tanglish_variations = ?, doc_link = ?, doc_title = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (question, answer, category, tanglish_variations, doc_link, doc_title, faq_id))
    conn.commit()
    conn.close()

    # Retrain model
    ai_engine.retrain()

    flash(f'FAQ #{faq_id} updated successfully and AI model retrained!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/faq/delete/<int:faq_id>', methods=['POST'])
@login_required
def delete_faq(faq_id):
    """Delete an FAQ and retrain model."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM faqs WHERE id = ?', (faq_id,))
    conn.commit()
    conn.close()

    ai_engine.retrain()
    flash(f'FAQ #{faq_id} deleted successfully.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/unknown/resolve/<int:query_id>', methods=['POST'])
@login_required
def resolve_unknown_query(query_id):
    """Mark unknown query as resolved with optional admin answer."""
    admin_answer = request.form.get('admin_answer', '').strip()
    status = request.form.get('status', 'Resolved')
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE unknown_queries 
        SET status = ?, admin_answer = ? 
        WHERE id = ?
    ''', (status, admin_answer, query_id))
    conn.commit()
    conn.close()

    flash(f'Query #{query_id} status updated to {status}.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/unknown/delete/<int:query_id>', methods=['POST'])
@login_required
def delete_unknown_query(query_id):
    """Delete an unknown query record."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM unknown_queries WHERE id = ?', (query_id,))
    conn.commit()
    conn.close()

    flash(f'Unknown query record #{query_id} deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/settings/update', methods=['POST'])
@login_required
def update_settings():
    """Update institutional configuration."""
    conn = get_db_connection()
    c = conn.cursor()
    for key, value in request.form.items():
        if key != 'csrf_token':
            c.execute('INSERT OR REPLACE INTO college_settings (key, value) VALUES (?, ?)', (key, value.strip()))
    conn.commit()
    conn.close()

    flash('College institutional settings updated successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/api/admin/chart-data', methods=['GET'])
@login_required
def admin_chart_data():
    """Provide real database-backed chart metrics for Chart.js in admin dashboard."""
    conn = get_db_connection()
    c = conn.cursor()

    # 1. Category distribution
    c.execute('SELECT category, COUNT(*) as count FROM faqs GROUP BY category')
    cat_rows = c.fetchall()
    categories = [r['category'] for r in cat_rows]
    category_counts = [r['count'] for r in cat_rows]

    # 2. Answered vs Unanswered queries
    c.execute("SELECT COUNT(*) FROM chat_history WHERE confidence >= 0.35")
    answered_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM unknown_queries WHERE status = 'Pending Review'")
    unanswered_count = c.fetchone()[0]

    # 3. Query volume by language
    c.execute("SELECT language, COUNT(*) as count FROM chat_history GROUP BY language")
    lang_rows = c.fetchall()
    languages = [r['language'] for r in lang_rows] or ['English', 'Tanglish']
    lang_counts = [r['count'] for r in lang_rows] or [0, 0]

    # 4. Top 5 Most asked intents
    c.execute('''
        SELECT intent, COUNT(*) as count 
        FROM chat_history 
        WHERE intent IS NOT NULL AND intent != 'unknown_query'
        GROUP BY intent 
        ORDER BY count DESC LIMIT 5
    ''')
    top_intents_rows = c.fetchall()
    top_intents = [r['intent'].replace('_', ' ').title() for r in top_intents_rows]
    top_intent_counts = [r['count'] for r in top_intents_rows]

    conn.close()

    return jsonify({
        'categories': categories,
        'category_counts': category_counts,
        'answered_vs_unanswered': {
            'labels': ['Answered by AI', 'Unanswered / Unknown'],
            'data': [answered_count, unanswered_count]
        },
        'languages': {
            'labels': languages,
            'data': lang_counts
        },
        'top_intents': {
            'labels': top_intents,
            'data': top_intent_counts
        }
    })

# ==========================================
# SERVER BOOTSTRAP
# ==========================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n========================================================")
    print(f"  College Chatbot Using AI - Server Starting")
    print(f"  URL: http://127.0.0.1:{port}")
    print(f"  Chatbot: http://127.0.0.1:{port}/chat")
    print(f"  Admin: http://127.0.0.1:{port}/admin/login (admin / admin123)")
    print(f"========================================================\n")
    app.run(host='0.0.0.0', port=port, debug=False)
