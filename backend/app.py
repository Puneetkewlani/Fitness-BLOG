from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

# Database configuration - handle both local and deployed environments
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'fitness_data.db')
PARENT_DIR = os.path.dirname(BASE_DIR)

# Initialize database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Fitness Assessment Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fitness_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                goal TEXT NOT NULL,
                fitness_level TEXT NOT NULL,
                email TEXT NOT NULL,
                workout_type TEXT,
                frequency TEXT,
                diet_preference TEXT,
                injuries_concerns TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Contact Form Submissions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                interest TEXT,
                message TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Wellness Assessment Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wellness_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                weight REAL,
                height REAL,
                fitness_level TEXT,
                goal TEXT,
                frequency TEXT,
                workout_type TEXT,
                injuries_concerns TEXT,
                stress_level INTEGER,
                sleep_quality TEXT,
                sleep_hours REAL,
                diet_preference TEXT,
                water_intake INTEGER,
                smoking TEXT,
                alcohol TEXT,
                motivation TEXT,
                challenges TEXT,
                additional_comments TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # BMI Calculator History
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                ip_address TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Routes

@app.route('/', methods=['GET'])
def index():
    try:
        return send_file(os.path.join(PARENT_DIR, 'index.html'))
    except:
        return jsonify({
            'status': 'success',
            'message': 'Fitness Backend API is running!',
            'endpoints': {
                'fitness_assessment': '/api/fitness-assessment',
                'contact': '/api/contact',
                'bmi_calculation': '/api/bmi',
                'admin_dashboard': '/admin/dashboard',
                'get_assessments': '/admin/assessments',
                'get_contacts': '/admin/contacts',
                'get_bmi_data': '/admin/bmi-data'
            }
        })

# Fitness Assessment Endpoint
@app.route('/api/fitness-assessment', methods=['POST'])
def submit_fitness_assessment():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'weight', 'height', 'goal', 'fitness_level', 'email', 'workout_type', 'frequency', 'diet_preference']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO fitness_assessments 
            (name, weight, height, goal, fitness_level, email, workout_type, frequency, diet_preference, injuries_concerns)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['weight'], data['height'], data['goal'], data['fitness_level'], data['email'], 
              data['workout_type'], data['frequency'], data['diet_preference'], data.get('injuries_concerns', '')))
        
        conn.commit()
        submission_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Fitness assessment submitted successfully!',
            'id': submission_id
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
# Wellness Assessment Endpoint
@app.route('/api/wellness-assessment', methods=['POST'])
def submit_wellness_assessment():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'weight', 'height', 'fitness_level', 'goal']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        motivation = ','.join(data.get('motivation', [])) if isinstance(data.get('motivation'), list) else data.get('motivation', '')
        challenges = ','.join(data.get('challenges', [])) if isinstance(data.get('challenges'), list) else data.get('challenges', '')
        
        cursor.execute('''
            INSERT INTO wellness_assessments 
            (name, email, age, gender, weight, height, fitness_level, goal, frequency, 
             workout_type, injuries_concerns, stress_level, sleep_quality, sleep_hours, 
             diet_preference, water_intake, smoking, alcohol, motivation, challenges, additional_comments)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['email'], data.get('age'), data.get('gender'),
            data.get('weight'), data.get('height'), data['fitness_level'],
            data['goal'], data.get('frequency'), data.get('workout_type'),
            data.get('injuries_concerns'), data.get('stress_level'),
            data.get('sleep_quality'), data.get('sleep_hours'),
            data.get('diet_preference'), data.get('water_intake'),
            data.get('smoking'), data.get('alcohol'),
            motivation, challenges, data.get('additional_comments', '')
        ))
        
        conn.commit()
        submission_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Wellness assessment submitted successfully!',
            'id': submission_id
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# Contact Form Endpoint
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'email', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contact_submissions (name, email, phone, interest, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], data.get('phone', ''), data.get('interest', ''), data['message']))
        
        conn.commit()
        submission_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Contact message submitted successfully!',
            'id': submission_id
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# BMI Calculation Endpoint
@app.route('/api/bmi', methods=['POST'])
def submit_bmi():
    try:
        data = request.get_json()
        
        if 'weight' not in data or 'height' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Weight and height are required'
            }), 400
        
        weight = float(data['weight'])
        unit_system = data.get('unit_system', 'metric')  # 'metric' or 'imperial'
        
        # Convert height to meters
        if unit_system == 'imperial':
            # feet and inches to meters
            feet = float(data.get('feet', 0))
            inches = float(data.get('inches', 0))
            height = (feet * 12 + inches) * 0.0254  # Convert to meters
            weight = weight * 0.453592  # Convert lbs to kg
        else:
            height = float(data['height']) / 100  # Convert cm to meters
        
        # Calculate BMI
        bmi = weight / (height ** 2)
        
        # Determine category
        if bmi < 18.5:
            category = 'Underweight'
        elif 18.5 <= bmi < 25:
            category = 'Normal weight'
        elif 25 <= bmi < 30:
            category = 'Overweight'
        else:
            category = 'Obese'
        
        conn = get_db()
        cursor = conn.cursor()
        
        ip_address = request.remote_addr
        cursor.execute('''
            INSERT INTO bmi_calculations (weight, height, bmi, category, ip_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (weight, height * 100, bmi, category, ip_address))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'bmi': round(bmi, 1),
            'category': category,
            'message': f'Your BMI is {round(bmi, 1)} - {category}'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Admin Dashboard
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get statistics
        cursor.execute('SELECT COUNT(*) as count FROM fitness_assessments')
        assessments_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM contact_submissions')
        contacts_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM bmi_calculations')
        bmi_count = cursor.fetchone()['count']
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'statistics': {
                'fitness_assessments': assessments_count,
                'contact_submissions': contacts_count,
                'bmi_calculations': bmi_count
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Get all fitness assessments
@app.route('/admin/assessments', methods=['GET'])
def get_assessments():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM fitness_assessments ORDER BY submitted_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        assessments = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'data': assessments,
            'count': len(assessments)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Get all contact submissions
@app.route('/admin/contacts', methods=['GET'])
def get_contacts():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM contact_submissions ORDER BY submitted_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        contacts = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'data': contacts,
            'count': len(contacts)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Get all BMI calculations
@app.route('/admin/bmi-data', methods=['GET'])
def get_bmi_data():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bmi_calculations ORDER BY submitted_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        bmi_data = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'data': bmi_data,
            'count': len(bmi_data)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    print("🚀 Starting Fitness Backend Server...")
    print(f"📍 Server running at port {port}")
    print(f"📊 Admin Dashboard available at your deployed URL")
    app.run(debug=debug_mode, port=port, host='0.0.0.0')
