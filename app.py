from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source_ip TEXT,
        event_type TEXT,
        description TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events ORDER BY timestamp DESC")
    events = c.fetchall()
    conn.close()
    return render_template('dashboard.html', events=events)

@app.route('/router_event', methods=['POST'])
def router_event():
    data = request.json
    if not data:
        return "No JSON received", 400
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("INSERT INTO events (timestamp, source_ip, event_type, description) VALUES (?, ?, ?, ?)",
              (datetime.utcnow().isoformat(), data.get("source_ip"), data.get("event_type"), data.get("description")))
    conn.commit()
    conn.close()
    return "Event received", 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
