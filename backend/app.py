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

# Helper function to load dotenv manually
def load_dotenv():
    paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    ]
    for dotenv_path in paths:
        if os.path.exists(dotenv_path):
            try:
                with open(dotenv_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
            except Exception as e:
                print(f"Error loading {dotenv_path}: {e}")

# Gemini API Integration
def call_gemini_api(prompt, api_key):
    import urllib.request
    import json
    
    models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
    system_instruction = (
        "You are FitLife AI, a friendly, encouraging, and professional fitness, nutrition, and wellness AI coach "
        "created by Puneet Kewlani. Your goal is to provide evidence-based, supportive, and practical advice on "
        "diets, workouts, weight loss/gain, and lifestyle habits. Keep your answers relatively concise, encouraging, "
        "and highly structured with bullet points or emojis when helpful. Always warn users to consult with "
        "medical professionals before starting extreme programs, especially if they have pre-existing injuries. "
        "Always reply in clean, well-formatted HTML (using tags like <p>, <ul>, <li>, <strong>, etc.) so it displays "
        "beautifully in the chat window, but do NOT wrap it in a markdown ```html code block."
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "systemInstruction": {
            "parts": [
                {"text": system_instruction}
            ]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800
        }
    }
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers=headers, 
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                text = res_data['candidates'][0]['content']['parts'][0]['text']
                return text
        except Exception as e:
            print(f"Gemini API Error with model {model}: {e}")
            continue
            
    return None

# Local expert chatbot fallback for seamless robust performance
def get_local_expert_response(msg):
    msg = msg.lower()
    
    if any(k in msg for k in ['hello', 'hi', 'hey', 'greetings', 'yo']):
        return (
            "<p>👋 <strong>Hello! I'm your FitLife AI Coach.</strong></p>"
            "<p>I'm here to help you guide through your health, exercise, and diet journey! "
            "Whether you need a custom workout, healthy meal ideas, or sleep tips, just ask.</p>"
            "<p>Here are some things you can try asking me:</p>"
            "<ul>"
            "<li><em>\"How do I lose weight safely?\"</em></li>"
            "<li><em>\"Give me a simple balanced meal plan.\"</em></li>"
            "<li><em>\"What are the best exercises for strength?\"</em></li>"
            "<li><em>\"How can I calculate my BMI?\"</em></li>"
            "</ul>"
        )
        
    elif any(k in msg for k in ['diet', 'food', 'eat', 'meal', 'nutrition', 'recipe', 'breakfast', 'lunch', 'dinner']):
        return (
            "<p>🥗 <strong>Nutrition & Diet Tips</strong></p>"
            "<p>A balanced diet is the cornerstone of sustainable health. Focus on whole foods and high-quality macronutrients:</p>"
            "<ul>"
            "<li><strong>Proteins:</strong> Vital for muscle repair. Include eggs, chicken, paneer, tofu, and legumes.</li>"
            "<li><strong>Carbohydrates:</strong> Your main energy source. Choose complex carbs like oats, brown rice, and sweet potatoes.</li>"
            "<li><strong>Fats:</strong> Essential for hormones. Opt for nuts, olive oil, and avocados.</li>"
            "</ul>"
            "<p>Check out our detailed <a href=\"diet.html\" style=\"color: #6366f1; text-decoration: underline;\">Diet Plans</a> page for sample macronutrient distributions, or fill out the <strong>Fitness Assessment</strong> on our home page to receive a fully customized plan in your inbox!</p>"
        )
        
    elif any(k in msg for k in ['workout', 'exercise', 'routine', 'gym', 'training', 'cardio', 'strength', 'stretch']):
        return (
            "<p>💪 <strong>Exercise & Training Guide</strong></p>"
            "<p>To see continuous progress, your routine should incorporate a mix of strength and cardiovascular training:</p>"
            "<ul>"
            "<li><strong>Strength Training:</strong> Builds calorie-burning muscle tissue and increases density. Try compound lifts like squats, deadlifts, and push-ups.</li>"
            "<li><strong>Cardiovascular Exercise:</strong> Improves heart health and boosts fat loss. Aim for 150 minutes of moderate activity (like brisk walking) per week.</li>"
            "<li><strong>Flexibility & Recovery:</strong> Never skip stretching. It prevents injuries and increases your range of motion.</li>"
            "</ul>"
            "<p>Explore full instructional guides on our <a href=\"exercise.html\" style=\"color: #6366f1; text-decoration: underline;\">Exercise Catalog</a>!</p>"
        )
        
    elif any(k in msg for k in ['bmi', 'body mass index', 'calculate weight']):
        return (
            "<p>📏 <strong>Body Mass Index (BMI)</strong></p>"
            "<p>BMI is a useful standard measure to categorize individuals into weight classifications (Underweight, Normal, Overweight, Obese):</p>"
            "<ul>"
            "<li><strong>Underweight:</strong> Below 18.5</li>"
            "<li><strong>Normal weight:</strong> 18.5 to 24.9</li>"
            "<li><strong>Overweight:</strong> 25.0 to 29.9</li>"
            "<li><strong>Obese:</strong> 30.0 and above</li>"
            "</ul>"
            "<p>We have a fully interactive calculator waiting for you! Scroll down on the <a href=\"diet.html#bmiResult\" style=\"color: #6366f1; text-decoration: underline;\">Diet Plans</a> page to enter your measurements and get instant feedback with local database saving.</p>"
        )
        
    elif any(k in msg for k in ['lose weight', 'weight loss', 'burn fat', 'slim down', 'calories', 'deficit']):
        return (
            "<p>🔥 <strong>Sustainable Fat Loss</strong></p>"
            "<p>The golden rule of fat loss is simple: you must create a <strong>calorie deficit</strong> (burning more calories than you consume). Here's a safe strategy:</p>"
            "<ol>"
            "<li><strong>Target Deficit:</strong> Aim for a mild deficit of 300 to 500 kcal below your daily maintenance level. This achieves about 0.5kg of healthy fat loss per week.</li>"
            "<li><strong>High Protein:</strong> Crucial to prevent muscle loss while losing weight. Make sure protein represents at least 30% of your daily intake.</li>"
            "<li><strong>NEAT (Activity):</strong> Walk more! Aiming for 8,000–10,000 steps daily is a massive contributor to fat loss.</li>"
            "</ol>"
            "<p><em>Note: Always consult a doctor before making any aggressive dietary modifications.</em></p>"
        )
        
    elif any(k in msg for k in ['gain muscle', 'build muscle', 'bulk', 'hypertrophy', 'size']):
        return (
            "<p>🏋️ <strong>Muscle Hypertrophy & Gain</strong></p>"
            "<p>To build clean muscle tissue, your body requires two main stimuli: a calorie surplus and progressive strength overload.</p>"
            "<ul>"
            "<li><strong>Calorie Surplus:</strong> Consume 200–400 calories *above* your maintenance level to provide building blocks.</li>"
            "<li><strong>Protein intake:</strong> Consume 1.6 to 2.2 grams of protein per kilogram of body weight.</li>"
            "<li><strong>Progressive Overload:</strong> Gradually increase the resistance (weights or reps) in your exercises over time to force adaptation.</li>"
            "<li><strong>Rest:</strong> Muscles grow when you rest, not when you lift. Get 7-8 hours of sleep.</li>"
            "</ul>"
        )
        
    elif any(k in msg for k in ['sleep', 'rest', 'recovery', 'insomnia', 'hours']):
        return (
            "<p>😴 <strong>Sleep & Recovery Protocol</strong></p>"
            "<p>Recovery is where the transformation happens. Without adequate rest, your body cannot heal and build muscle tissues efficiently:</p>"
            "<ul>"
            "<li><strong>Aim for 7-9 Hours:</strong> Consistent sleep cycles regulate critical fat-burning and growth hormones.</li>"
            "<li><strong>Sleep Hygiene:</strong> Discontinue phone/screen usage at least 45 minutes before bed. Keep your room dark, cool, and quiet.</li>"
            "<li><strong>Active Recovery:</strong> On rest days, do light walking or yoga to promote blood flow and alleviate soreness.</li>"
            "</ul>"
        )
        
    elif any(k in msg for k in ['injury', 'pain', 'hurt', 'sore', 'knees', 'back']):
        return (
            "<p>⚠️ <strong>Injury Care & Safety First</strong></p>"
            "<p>Your safety is the highest priority! If you feel sharp pain (distinguished from normal muscle soreness):</p>"
            "<ul>"
            "<li><strong>STOP immediately:</strong> Never 'push through' acute joint or tendon pain.</li>"
            "<li><strong>Use R.I.C.E.:</strong> Rest, Ice, Compression, and Elevation for minor strains.</li>"
            "<li><strong>Consult a professional:</strong> For any persistent joint pain, visit a licensed physician or physical therapist.</li>"
            "</ul>"
            "<p>When performing workouts, you can specify your injuries in our home page assessment so we exclude dangerous exercises from your routines.</p>"
        )
        
    else:
        return (
            "<p>💡 <strong>Thanks for your question!</strong></p>"
            "<p>As your FitLife Coach, I want to make sure you get the most accurate support. "
            "To give you custom diet and training recommendations tailored precisely to your metrics, "
            "please complete our <a href=\"index.html#assessment\" style=\"color: #6366f1; text-decoration: underline;\">Personalized Fitness Assessment</a>!</p>"
            "<p>You can also ask me about topics like: <strong>dieting, muscle gain, burning fat, sleep, exercise guides, and BMI calculations.</strong></p>"
        )

# AI Chatbot endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Message is required'
            }), 400
        
        user_message = data['message']
        
        # Load dotenv to find key
        load_dotenv()
        api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
        
        if api_key:
            # Attempt to call Gemini API
            gemini_response = call_gemini_api(user_message, api_key)
            if gemini_response:
                return jsonify({
                    'status': 'success',
                    'response': gemini_response,
                    'source': 'gemini'
                }), 200
        
        # Graceful fallback to smart local expert bot if API key is missing or call fails
        fallback_response = get_local_expert_response(user_message)
        return jsonify({
            'status': 'success',
            'response': fallback_response,
            'source': 'local_expert'
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

init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    print("🚀 Starting Fitness Backend Server...")
    print(f"[*] Server running at port {port}")
    print("[*] Admin Dashboard available at your deployed URL")
    app.run(debug=debug_mode, port=port, host='0.0.0.0')

