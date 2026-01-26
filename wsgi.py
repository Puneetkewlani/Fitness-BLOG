"""
WSGI entry point for Railway deployment
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the Flask app
from app import app

if __name__ == '__main__':
    app.run()
