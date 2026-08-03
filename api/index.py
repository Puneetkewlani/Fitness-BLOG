import os
import sys

# Add project root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app

# Export the Flask WSGI application for Vercel Serverless Functions
app = app
