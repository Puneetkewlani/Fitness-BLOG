🚂 RAILWAY DEPLOYMENT GUIDE
===========================

## What is Railway?

Railway is a modern platform-as-a-service (PaaS) that makes it easy to deploy web applications.
It automatically detects your project type and deploys it with minimal configuration.

Website: https://railway.app

## ✨ Advantages of Railway

✅ Free tier available ($5 free credit monthly)
✅ Automatic deployments from Git
✅ Environment variables support
✅ One-click deployment
✅ GitHub integration
✅ Database support (PostgreSQL, MongoDB, MySQL)
✅ Custom domains
✅ SSL certificates included
✅ Beautiful dashboard

## 📋 Prerequisites

1. GitHub account (Your repo is already there!)
2. Railway account (free signup)
3. Git installed (you have this)

## 🚀 DEPLOYMENT STEPS (Easy - 5 Minutes)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click "Sign Up"
3. Click "Continue with GitHub"
4. Authorize Railway
5. Confirm email

### Step 2: Create New Project
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Click "Deploy from GitHub repo"
4. Select your repository: "Fitness-BLOG"
5. Click "Deploy"

Railway will automatically:
✅ Detect Python project
✅ Read Procfile
✅ Install dependencies from requirements.txt
✅ Deploy backend automatically

### Step 3: Wait for Deployment
Railway will show a deployment progress log.
Wait until you see: "Build Complete ✓"

### Step 4: Get Your Live URL
In the Railway dashboard:
1. Click your project
2. Go to "Deployments" tab
3. Find "Public URL" (example: https://fitness-blog-prod.up.railway.app)
4. Click the link to test!

### Step 5: Update Frontend URLs (Optional)
Your frontend files are already configured to use localhost:5000 during development.

For production, update API URLs in:
- index.html (line ~669): `const API_URL = 'http://localhost:5000'`
- Contact.html (line ~523): `const API_URL = 'http://localhost:5000'`
- diet.html (line ~759): `const API_URL = 'http://localhost:5000'`

Change to your Railway URL:
```javascript
const API_URL = 'https://your-railway-app.up.railway.app'
```

## 📱 Access Your Live Website

### Backend API (Admin Dashboard):
https://your-railway-app.up.railway.app/admin/dashboard

### Frontend:
Serve from your own web hosting or on Railway static service

## 🗄️ Database Persistence

Your SQLite database (fitness_data.db) will be:
✅ Created automatically on first deployment
✅ Persisted across deployments
✅ Accessible via API endpoints

## 🔧 Environment Variables

Railway automatically handles these, but you can customize:

1. Go to project settings
2. Click "Variables"
3. Add custom variables:

```
FLASK_DEBUG=False        # Disable debug mode in production
PORT=5000                # Railway assigns automatically
```

## 🚀 Auto-Deployment from GitHub

Railway automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update website"
git push origin main
```

Railway will automatically detect changes and redeploy!

## 📊 Monitor Your Deployment

In Railway dashboard:
- Logs: See real-time server logs
- Metrics: CPU, RAM, network usage
- Deployments: Deployment history
- Settings: Configure your app

## 🔐 Custom Domain (Optional)

1. In Railway project settings
2. Click "Domains"
3. Add custom domain (fitness-website.com)
4. Update DNS records at your domain provider

## 💰 Costs

Free Tier:
- $5 credit monthly
- Up to 500 MB storage
- Sufficient for small projects

Paid (if needed):
- Pay-as-you-go after free tier
- ~$2-5/month for small app

## 🚨 Troubleshooting

### Build Failed?
1. Check logs in Railway dashboard
2. Make sure requirements.txt has all dependencies
3. Check Procfile syntax
4. Verify Python version in runtime.txt

### Application won't start?
1. Check app.py for syntax errors
2. Verify database initialization
3. Check environment variables
4. View logs in Railway: Deployments > Logs

### Database not persisting?
1. SQLite files persist between deployments
2. Make sure app.py creates database correctly
3. Don't delete fitness_data.db

### CORS errors?
Check the app.py has: `CORS(app)` (it does!)

## 📝 Deployment Checklist

- ✅ Procfile created
- ✅ runtime.txt created
- ✅ .railwayignore created
- ✅ app.py updated for environment variables
- ✅ requirements.txt has all dependencies
- ✅ Git repository pushed
- ✅ Railway account created
- ✅ Project deployed
- ✅ Live URL working
- ✅ Admin dashboard accessible

## 🎯 Next Steps

1. Create Railway account
2. Deploy project
3. Test admin dashboard
4. Update frontend URLs (if needed)
5. Share your live website!

## 📞 Support

Railway Help: https://railway.app/docs
GitHub Discussions: https://github.com/railwayapp

---

Your Fitness Website is Ready for the World! 🌍

Once deployed, your website will be live 24/7! 🎉
