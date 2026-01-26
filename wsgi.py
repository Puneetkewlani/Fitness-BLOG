"""
WSGI entry point for Railway deployment
"""
import sys
import os

# Get the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(CURRENT_DIR, 'backend')

# Add backend directory to path
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Import the Flask app from backend.app module
from app import app

if __name__ == '__main__':
    app.run()
