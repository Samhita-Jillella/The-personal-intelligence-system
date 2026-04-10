from flask import Flask, render_template, jsonify,request
from analytics import analytics_bp
import sqlite3

app = Flask(__name__)
app.register_blueprint(analytics_bp)

DATABASE = 'database.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test')
def test_api():
    return jsonify({'message': 'Backend is running!', 'status': 'success'})

# Create and return a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create the logs table if it does not exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            sleep_hours REAL,
            mood INTEGER,
            energy INTEGER,
            work_hours REAL,
            exercise_minutes INTEGER,
            stress INTEGER,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()

# Create a new daily log
@app.route('/api/log', methods=['POST'])
def create_log():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data received'
            }), 400

        date = data.get('date')
        sleep_hours = data.get('sleep_hours')
        mood = data.get('mood')
        energy = data.get('energy')
        work_hours = data.get('work_hours')
        exercise_minutes = data.get('exercise_minutes')
        stress = data.get('stress')
        notes = data.get('notes')

        if not date:
            return jsonify({
                'status': 'error',
                'message': 'date is required'
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO logs (
                date, sleep_hours, mood, energy,
                work_hours, exercise_minutes, stress, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date, sleep_hours, mood, energy,
            work_hours, exercise_minutes, stress, notes
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Log created successfully',
            'id': new_id
        }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to create log',
            'error': str(e)
        }), 500

@app.route("/logs")
def get_logs():
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM logs").fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

# Update an existing log by id
@app.route('/api/log/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data received'
            }), 400

        date = data.get('date')
        sleep_hours = data.get('sleep_hours')
        mood = data.get('mood')
        energy = data.get('energy')
        work_hours = data.get('work_hours')
        exercise_minutes = data.get('exercise_minutes')
        stress = data.get('stress')
        notes = data.get('notes')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE logs
            SET date = ?, sleep_hours = ?, mood = ?, energy = ?,
                work_hours = ?, exercise_minutes = ?, stress = ?, notes = ?
            WHERE id = ?
        """, (
            date, sleep_hours, mood, energy,
            work_hours, exercise_minutes, stress, notes, log_id
        ))

        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                'status': 'error',
                'message': 'Log not found'
            }), 404

        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Log updated successfully'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to update log',
            'error': str(e)
        }), 500


# Delete a log by id
@app.route('/api/log/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                'status': 'error',
                'message': 'Log not found'
            }), 404

        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Log deleted successfully'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete log',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
