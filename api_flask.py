from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv('API_KEY')

def authenticate(key):
    return key == API_KEY

@app.route('/analyze', methods=['GET'])
def analyze():
    key = request.headers.get('API_KEY')
    if not authenticate(key):
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({"message": "API key authorized."})

@app.route('/')
def index():
    return 'Welcome to the Web Server Log Analysis API!'

if __name__ == '__main__':
    app.run(debug=True)
