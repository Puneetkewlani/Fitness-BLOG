🚀 BACKEND SERVER - QUICK START GUIDE
=====================================

## 🎯 Your Backend is Ready!

A complete backend system has been set up to store all form submissions from your fitness website.

---

## ⚡ Quick Start (Copy & Paste)

Open PowerShell and run these commands:

```powershell
cd c:\Users\LENOVO\IWT-Project-\backend
python app.py
```

That's it! Your server is now running at: http://localhost:5000

---

## 🎨 Access Admin Dashboard

After starting the server, open your browser and visit:

👉 http://localhost:5000/admin/dashboard

You'll see:
✅ Statistics (total submissions)
✅ Fitness assessments (with user data)
✅ Contact submissions (with messages)
✅ BMI calculations (with results)

---

## 📝 What's Connected

✅ **Homepage** - Fitness assessment form
✅ **Diet Page** - BMI calculator  
✅ **Contact Page** - Contact form

All form submissions are automatically stored in the database!

---

## 🗄️ Database

Location: c:\Users\LENOVO\IWT-Project-\backend\fitness_data.db

Tables:
- fitness_assessments (homepage form)
- contact_submissions (contact page)
- bmi_calculations (diet page calculator)

---

## 🛑 To Stop the Server

In the terminal, press: CTRL + C

---

## 🐛 Troubleshooting

❌ "Connection refused"?
   → Make sure you ran `python app.py` first

❌ "Module not found"?
   → Run: python -m pip install -r requirements.txt

❌ "Port 5000 in use"?
   → Close other Flask apps or edit app.py line 255 to use a different port

---

## 📊 Data Files

- app.py - Main backend application
- admin_dashboard.html - Dashboard interface
- fitness_data.db - SQLite database (auto-created)
- requirements.txt - Dependencies

---

## 📚 Documentation

For detailed info, see: BACKEND_SETUP.md

---

## 💡 Pro Tips

1. **Keep server running** while testing your website
2. **Browser cache** - Press F5 to refresh if needed
3. **Check console** - Press F12 in browser to see any errors
4. **Export data** - All data is in the database, easy to backup!

---

Created: January 26, 2025
Status: ✅ Ready to use!
