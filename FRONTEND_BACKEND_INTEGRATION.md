🌐 FRONTEND & BACKEND INTEGRATION FOR PRODUCTION
=================================================

## How to Connect Frontend to Your Live Backend

After deploying to Railway, you need to connect your frontend files to the live backend.

## Option 1: Update HTML Files (Recommended)

### Step 1: Get Your Railway URL

After deployment on Railway, you'll have a URL like:
`https://fitness-blog-prod-abc123.up.railway.app`

### Step 2: Update API URLs in HTML Files

Update the `API_URL` variable in these files:

#### File 1: index.html (Line ~669)
```javascript
// OLD:
const API_URL = 'http://localhost:5000';

// NEW:
const API_URL = 'https://YOUR-RAILWAY-URL.up.railway.app';
```

#### File 2: contact.html (Line ~523)
```javascript
// OLD:
const API_URL = 'http://localhost:5000';

// NEW:
const API_URL = 'https://YOUR-RAILWAY-URL.up.railway.app';
```

#### File 3: diet.html (Line ~759)
```javascript
// OLD:
const API_URL = 'http://localhost:5000';

// NEW:
const API_URL = 'https://YOUR-RAILWAY-URL.up.railway.app';
```

### Step 3: Commit and Push

```bash
git add .
git commit -m "Updated API URLs for production deployment"
git push origin main
```

Railway will automatically redeploy!

## Option 2: Serve Frontend from Same Server

If you want to serve frontend and backend from the same Railway instance:

1. Update `backend/app.py` to serve static files:

```python
from flask import Flask, send_from_directory
import os

app = Flask(__name__, 
    static_folder='..', 
    static_url_path='',
    template_folder='..')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.endswith('.html'):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, path)
```

2. Update API URL to relative path in HTML:

```javascript
const API_URL = '/api';  // Same domain!
```

3. Update endpoints in app.py (change /api/... to /api/...)

## Accessing Your Live Website

### Admin Dashboard
https://YOUR-RAILWAY-URL.up.railway.app/admin/dashboard

### Frontend (if served from Railway)
https://YOUR-RAILWAY-URL.up.railway.app/

### Frontend (if served separately)
Host files on:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting

## Testing in Production

1. Open your Railway URL in browser
2. Fill out a form (fitness assessment, contact, or BMI)
3. Check the admin dashboard
4. Verify data appears

## Troubleshooting Production

### CORS Errors?
- Make sure `CORS(app)` is in app.py ✓
- Check API_URL matches your Railway URL
- Clear browser cache (Ctrl+Shift+Delete)

### Forms not submitting?
- Check browser console (F12)
- Verify API_URL is correct
- Check Railway logs for errors

### Database empty?
- First deployment creates fresh database
- Data persists after that
- Check API endpoints are working

## Environment-Specific Configuration

Create a config.js file for easier switching:

```javascript
// config.js
const CONFIG = {
    development: {
        API_URL: 'http://localhost:5000'
    },
    production: {
        API_URL: 'https://your-railway-url.up.railway.app'
    }
};

const API_URL = window.location.hostname === 'localhost' 
    ? CONFIG.development.API_URL 
    : CONFIG.production.API_URL;
```

## Quick Deployment Workflow

1. Make changes locally
2. Test with `python backend/app.py`
3. Update API URLs if changed
4. Push to GitHub
5. Railway automatically deploys
6. Check Railway logs
7. Test live version

## Still Using Local?

To keep using localhost for development:
- Don't update API URLs
- Keep backend server running: `python backend/app.py`
- Open: `http://localhost:5000/admin/dashboard`

## Production Best Practices

✅ Use environment variables for API URL
✅ Disable debug mode in production
✅ Use HTTPS (Railway provides this)
✅ Keep sensitive data in .env
✅ Monitor error logs
✅ Test thoroughly before deployment
✅ Keep backups of database

---

Ready to go live! 🚀
