import os
from flask import Flask, jsonify, send_from_directory
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

# Configuration
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', Config.MONGO_URI)
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET', Config.JWT_SECRET)

# Initialize extensions
mongo = PyMongo(app)
CORS(app)  # Enable CORS for development

# Serve React frontend in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# Your API routes here (from previous code)
# ... (include all your route blueprints)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
