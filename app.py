from flask import Flask, request, render_template, jsonify
import requests
import os
import json

app = Flask(__name__)
API_KEY = os.getenv('EDEN_AI_API_KEY')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resumeFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['resumeFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'providers': ['affinda'],  
        "language": "en",
        "fallback_providers": ""
    }

    files = {
        'file': (file.filename, file.read(), 'application/octet-stream')
    }
    
    response = requests.post(
        'https://api.edenai.run/v2/ocr/resume_parser',
        headers=headers,
        data=data,
        files=files
    )

    if response.status_code == 200:
        print("checking")
        result = json.loads(response.text)
        return jsonify(response.json())
    else:
        app.logger.error(f"Error from Eden AI: {response.text}")
        return jsonify({'error': 'Failed to parse resume', 'status_code': response.status_code, 'message': response.text}), response.status_code
    
if __name__ == '__main__':
    app.run(debug=True)
