from flask import Flask, request, jsonify
import psycopg2 as pg
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db():
    conn = pg.connect(DATABASE_URL)
    return conn

@app.route('/api/signups', methods=['POST'])
def add_signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO signups (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        return jsonify({"status": "success"}), 201
    except pg.IntegrityError:
        conn.rollback()
        return jsonify({"error": "Email must be unique"}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/api/signups', methods=['GET'])
def get_signups():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM signups")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    signups = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
    return jsonify(signups)

if __name__ == '__main__':
    app.run(debug=True)
