from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5500"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return '', 200

    app.logger.debug(f"Received request: {request.method} {request.path}")
    app.logger.debug(f"Request headers: {request.headers}")

    # Check if a file was included in the request
    if 'pdf_file' not in request.files:
        app.logger.error("No file part in request")
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['pdf_file']

    # Check if a file was selected
    if file.filename == '':
        app.logger.error("No file selected")
        return jsonify({"error": "No file selected"}), 400

    # Validate file type
    if not allowed_file(file.filename):
        app.logger.error("Invalid file type")
        return jsonify({"error": "Invalid file type. Only PDF files are allowed"}), 400

    try:
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        app.logger.info(f"File saved successfully: {filepath}")
        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename
        }), 200

    except Exception as e:
        app.logger.error(f"Error saving file: {str(e)}")
        return jsonify({"error": "Failed to save file"}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)