from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'host': os.getenv('MYSQL_HOST', 'mysql'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'root'),
    'database': os.getenv('MYSQL_DB', 'devops')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', messages=messages)
    except Exception as e:
        return f"Error: {e}"

@app.route('/add', methods=['POST'])
def add_message():
    message = request.form.get('message')
    if message:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (message) VALUES (%s)', (message,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            return f"Error: {e}"
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
