from flask import Flask, render_template_string, jsonify
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

# Парсим DB_PARAMS из строки окружения
db_params_str = os.getenv("DB_PARAMS")
db_params_dict = {}
for part in db_params_str.split():
    key, value = part.split("=", 1)
    db_params_dict[key] = value

DB_PARAMS = db_params_dict


import time

def init_db(retries=10, delay=2):
    for i in range(retries):
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS weather (city TEXT, temperature INT)''')
            
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully!")
            return
        except Exception as e:
            print(f"Database connection failed ({i+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Could not connect to the database after several attempts.")

@app.route('/ping')
def ping():
    return '<h1>PONG</h1>'

@app.route('/health')
def health():
    return jsonify({"status": "HEALTHY"})

@app.route('/list')
def list_weather():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT city, temperature FROM weather')
        records = cur.fetchall()
        cur.close()
        conn.close()


        if not records:
            return '<h1>Погода</h1><p>Нет данных в таблице.</p>'

        html = '<h1>Погода</h1><ul>'
        for rec in records:
            html += f'<li>{rec["city"]}: {rec["temperature"]}°C</li>'
        html += '</ul>'
        return html

    except Exception as e:
        return f"<h1>Ошибка</h1><pre>{e}</pre>"

@app.route('/add', methods=['POST'])
def add_weather():
    data = request.get_json()
    city = data.get('city')
    temperature = data.get('temperature')
    if not city or temperature is None:
        return jsonify({'status': 'error', 'message': 'city and temperature required'}), 400

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute('INSERT INTO weather (city, temperature) VALUES (%s, %s)', (city, temperature))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Record added'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
