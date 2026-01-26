from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

# Add this route to serve the homepage
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.endswith('.html'):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, path)

# DATABASE SETUP CONTINUES AS BEFORE...
