from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from utils.validator import validate_excel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Keep the upload folder

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file to the upload folder (no file extension check)
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Validate the Excel file (you can still validate the file's contents if needed)
    validation_result = validate_excel(filepath)
    os.remove(filepath)  # Clean up after validation

    return jsonify(validation_result)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure the upload folder exists
    app.run(debug=True)
