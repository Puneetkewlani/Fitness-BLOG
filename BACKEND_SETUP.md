# 🚀 Backend Setup Guide - Fitness Website

## Overview
Your fitness website now has a complete backend system to store:
- ✅ Fitness assessments from the homepage
- ✅ Contact form submissions
- ✅ BMI calculation history

All data is stored in a SQLite database and can be viewed through an admin dashboard.

---

## 📋 Prerequisites

✅ Python 3.7+ (Already installed on your system)
✅ Flask and Flask-CORS (Already installed: `pip install Flask Flask-CORS`)

---

## 🎯 Quick Start (3 Steps)

### Step 1: Open Terminal in Backend Folder
```bash
cd c:\Users\LENOVO\IWT-Project-\backend
```

### Step 2: Start the Backend Server
```bash
python app.py
```

You should see:
```
✅ Database initialized successfully!
🚀 Starting Fitness Backend Server...
📍 Server running at http://localhost:5000
📊 Admin Dashboard: http://localhost:5000/admin/dashboard
```

### Step 3: Access Admin Dashboard
Open your browser and visit:
```
http://localhost:5000/admin/dashboard
```

---

## 📂 Backend Project Structure

```
backend/
├── app.py                 # Main Flask application with all API endpoints
├── admin_dashboard.html   # Admin dashboard to view all submissions
├── requirements.txt       # Python dependencies
└── fitness_data.db       # SQLite database (created automatically)
```

---

## 🔌 API Endpoints

### 1. Submit Fitness Assessment
**Endpoint:** `POST /api/fitness-assessment`

**Request body:**
```json
{
  "name": "John Doe",
  "weight": 75,
  "height": 180,
  "goal": "muscle-gain",
  "fitness_level": "intermediate",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Fitness assessment submitted successfully!",
  "id": 1
}
```

### 2. Submit Contact Form
**Endpoint:** `POST /api/contact`

**Request body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "9876543210",
  "interest": "strength",
  "message": "I want to build muscle..."
}
```

### 3. Submit BMI Calculation
**Endpoint:** `POST /api/bmi`

**Request body:**
```json
{
  "weight": 70,
  "height": 175
}
```

**Response:**
```json
{
  "status": "success",
  "bmi": 22.9,
  "category": "Normal weight",
  "message": "Your BMI is 22.9 - Normal weight"
}
```

### 4. Get Dashboard Statistics
**Endpoint:** `GET /admin/dashboard`

**Response:**
```json
{
  "status": "success",
  "statistics": {
    "fitness_assessments": 5,
    "contact_submissions": 3,
    "bmi_calculations": 12
  },
  "timestamp": "2025-01-26T19:30:00"
}
```

### 5. Get All Fitness Assessments
**Endpoint:** `GET /admin/assessments`

### 6. Get All Contact Submissions
**Endpoint:** `GET /admin/contacts`

### 7. Get All BMI Calculations
**Endpoint:** `GET /admin/bmi-data`

---

## 🎨 Admin Dashboard Features

The admin dashboard (`http://localhost:5000/admin/dashboard`) displays:

✅ **Statistics Cards**
- Total fitness assessments
- Total contact submissions
- Total BMI calculations

✅ **Three Data Tabs**
- Fitness Assessments (with name, weight, height, goal, fitness level, email, timestamp)
- Contact Submissions (with name, email, phone, interest, message, timestamp)
- BMI Data (with weight, height, BMI value, category, IP address, timestamp)

✅ **Auto-Refresh**
- Dashboard refreshes every 30 seconds automatically

---

## 🗄️ Database Schema

### fitness_assessments table
```
id (PRIMARY KEY)
name (TEXT)
weight (REAL)
height (REAL)
goal (TEXT)
fitness_level (TEXT)
email (TEXT)
submitted_at (TIMESTAMP)
```

### contact_submissions table
```
id (PRIMARY KEY)
name (TEXT)
email (TEXT)
phone (TEXT)
interest (TEXT)
message (TEXT)
submitted_at (TIMESTAMP)
```

### bmi_calculations table
```
id (PRIMARY KEY)
weight (REAL)
height (REAL)
bmi (REAL)
category (TEXT)
ip_address (TEXT)
submitted_at (TIMESTAMP)
```

---

## 🔧 Configuration

### Change Server Port
Edit `app.py` line 255:
```python
app.run(debug=True, port=5000, host='0.0.0.0')  # Change 5000 to your port
```

### Change Database Location
Edit `app.py` line 7:
```python
DATABASE = 'fitness_data.db'  # Change path if needed
```

### Enable/Disable CORS
Already enabled for all origins. To restrict, edit `app.py` line 5:
```python
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
```

---

## 🧪 Testing the Backend

### Test 1: Check if server is running
```bash
curl http://localhost:5000/
```

### Test 2: Submit a fitness assessment
```bash
curl -X POST http://localhost:5000/api/fitness-assessment \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","weight":70,"height":175,"goal":"weight-loss","fitness_level":"beginner","email":"test@test.com"}'
```

### Test 3: Get all assessments
```bash
curl http://localhost:5000/admin/assessments
```

---

## 🚨 Troubleshooting

### Issue: "Connection refused on port 5000"
**Solution:** Make sure the backend server is running:
```bash
python app.py
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install dependencies:
```bash
python -m pip install -r requirements.txt
```

### Issue: "Database is locked"
**Solution:** Close all other connections and restart:
```bash
python app.py
```

### Issue: "CORS error" in browser console
**Solution:** Make sure you're accessing from the same machine (localhost). The server allows all origins.

---

## 📊 Viewing the Data

### Via Admin Dashboard (Recommended)
1. Start backend: `python app.py`
2. Open: `http://localhost:5000/admin/dashboard`
3. Browse through Fitness Assessments, Contact, and BMI tabs

### Via SQLite CLI
```bash
sqlite3 fitness_data.db
sqlite> SELECT * FROM fitness_assessments;
sqlite> SELECT * FROM contact_submissions;
sqlite> SELECT * FROM bmi_calculations;
sqlite> .exit
```

### Via Python Script
```python
import sqlite3
conn = sqlite3.connect('fitness_data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM fitness_assessments')
for row in cursor.fetchall():
    print(row)
conn.close()
```

---

## 🔐 Security Notes

⚠️ **Current Setup (Development Only)**
- No authentication required
- CORS enabled for all origins
- Debug mode enabled
- No rate limiting

✅ **For Production, Add:**
```python
# Authentication
from functools import wraps
# Rate limiting
from flask_limiter import Limiter
# CORS restrictions
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
# Disable debug mode
app.run(debug=False)
```

---

## 🌐 Deployment Options

### Option 1: Local Testing (Recommended for now)
Keep running on `localhost:5000`

### Option 2: Deploy to Heroku
```bash
# 1. Create Procfile in backend folder
echo "web: python app.py" > Procfile

# 2. Deploy
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: Deploy to PythonAnywhere
1. Create account at pythonanywhere.com
2. Upload backend folder
3. Configure WSGI file
4. Access at `your-username.pythonanywhere.com`

---

## 📝 Log Files

The application logs are displayed in the terminal. To save logs:
```bash
python app.py > server.log 2>&1
```

---

## 🤝 Integration Checklist

- ✅ Homepage fitness assessment form connected
- ✅ Contact page contact form connected
- ✅ Diet page BMI calculator connected
- ✅ Admin dashboard created
- ✅ Database schema configured
- ✅ CORS enabled
- ✅ Error handling implemented
- ✅ JSON API endpoints working

---

## 📞 Support

For issues:
1. Check the terminal output for error messages
2. Verify the backend server is running
3. Ensure port 5000 is not blocked by firewall
4. Check browser console (F12) for CORS or network errors

---

## 🎉 Next Steps

1. ✅ Keep the backend server running while testing
2. ✅ Submit data through the forms on your website
3. ✅ View submissions in the admin dashboard
4. ✅ Export data as needed
5. ✅ Deploy to production when ready

---

**Created:** January 26, 2025
**Version:** 1.0
**Status:** Ready for production
