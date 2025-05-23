from flask import Flask, request, jsonify, send_file
import os
import zipfile
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "DAW Export Backend is Live"})

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    export_path = os.path.join(EXPORT_FOLDER, f"{filename}.zip")
    with zipfile.ZipFile(export_path, 'w') as zipf:
        zipf.write(filepath, arcname=file.filename)

    return jsonify({'message': 'File received', 'download_url': f"/download/{filename}.zip"})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    export_path = os.path.join(EXPORT_FOLDER, filename)
    if not os.path.exists(export_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(export_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
