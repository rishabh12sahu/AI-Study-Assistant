import os
import hashlib
from flask import Flask, render_template, request, redirect, session, url_for
import oracledb

# Import database and RAG logic
from database.oracle_db import get_connection
from ingestion.extract_pdf import extract_text
from ingestion.chunk_text import chunk_text
from ingestion.generate_embedding import generate_embeddings, embed_query
from database.store_oracle import store_embeddings
from database.search_oracle import search_chunks
from llm import ask_llm

app = Flask(__name__)
app.secret_key = "ai_study_assistant_secret_key_99"

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- ROUTES ---

# 1. LOGIN PAGE / LANDING
@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('upload_page'))
    return render_template('index.html')

# 2. SIGNUP PAGE
@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

# 3. HANDLE SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_pw = hash_password(password)

    conn = get_connection()
    if not conn: 
        return "❌ DB Connection Error"

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (:1, :2, :3)", 
            [username, email, hashed_pw]
        )
        conn.commit()
        return redirect(url_for('index'))
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1:
            return "❌ An account with this email already exists. Please log in.", 400
        return f"❌ Signup Error: {error.message}", 400
    except Exception as e:
        return f"❌ Signup Error: {e}", 400
    finally:
        cursor.close()
        conn.close()

# 4. HANDLE LOGIN (FIXED: Saving session & redirecting to upload_page)
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_pw = hash_password(password)
    
    conn = get_connection()
    if not conn: 
        return "❌ DB Connection Error"
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT username, email FROM users WHERE email = :1 AND password_hash = :2", 
            [email, hashed_pw]
        )
        user = cursor.fetchone()
        
        if user:
            # Save login state in Flask session
            session['username'] = user[0]
            session['email'] = user[1]
            return redirect(url_for('upload_page'))
        else:
            return "❌ Invalid email or password", 401
    except Exception as e:
        return f"❌ Login Error: {e}"
    finally:
        cursor.close()
        conn.close()

# 5. UPLOAD PAGE
@app.route('/upload_page')
def upload_page():
    if 'email' not in session: 
        return redirect(url_for('index'))
    return render_template('upload.html')

# 6. HANDLE PDF UPLOAD & PROCESSING
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'email' not in session:
        return redirect(url_for('index'))
        
    file = request.files['file']
    user_email = session['email']

    if file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Start RAG Pipeline
        text = extract_text(file_path)
        chunks = chunk_text(text)
        embeddings = generate_embeddings(chunks)
        
        store_embeddings(chunks, embeddings, user_email)
        
        return redirect(url_for('query_page'))
    return "No file selected"

# 7. QUERY PAGE
@app.route('/query_page')
def query_page():
    if 'email' not in session: 
        return redirect(url_for('index'))
    return render_template('querry.html')

# 8. HANDLE AI QUESTION
@app.route('/ask', methods=['POST'])
def ask():
    if 'email' not in session: 
        return redirect(url_for('index'))
        
    user_question = request.form.get('question')
    user_email = session['email']
    
    # 1. Vectorize query
    query_embedding = embed_query(user_question)

    # 2. Search Oracle DB
    results = search_chunks(query_embedding, user_email, top_k=6)
    
    if not results:
        return render_template('querry.html', question=user_question, answer="I couldn't find any information in your documents.")

    # 3. Get Answer from LLM
    context = "\n---\n".join(results)
    answer = ask_llm(user_question, context)
    
    return render_template('querry.html', question=user_question, answer=answer)

# 9. LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)