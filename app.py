
from flask import Flask, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
# Recreate database if missing columns
def check_and_reset_db():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    try:
        c.execute("SELECT router_name FROM events LIMIT 1")
    except sqlite3.OperationalError:
        print("router_name column missing — recreating DB...")
        conn.close()
        os.remove('events.db')
        init_db()
    else:
        conn.close()

check_and_reset_db()
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            router_name TEXT,
            source_ip TEXT,
            event_type TEXT,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('SELECT router_name, source_ip, event_type, description, timestamp FROM events ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', events=rows)

@app.route('/router_event', methods=['POST'])
def router_event():
    data = request.get_json()
    router_name = data.get('router_name', 'Unknown Router')
    source_ip = data.get('source_ip')
    event_type = data.get('event_type')
    description = data.get('description')

    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('INSERT INTO events (router_name, source_ip, event_type, description) VALUES (?, ?, ?, ?)',
              (router_name, source_ip, event_type, description))
    conn.commit()
    conn.close()

    return {'status': 'success'}, 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
