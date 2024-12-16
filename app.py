from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from utils.validator import validate_excel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Keep the upload folder


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("Request received: Checking for 'file' key in request.files...")

        # Check if 'file' is in the request
        if 'file' not in request.files:
            print("Error: 'file' key not found in request.files")
            print("Request files received:", request.files)
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        print("File key found. Checking filename...")

        # Check if the file name is empty
        if file.filename == '':
            print("Error: No file selected")
            return jsonify({"error": "No file selected"}), 400

        # Log the filename received
        print(f"Received file: {file.filename}")

        # Secure the filename and create the file path
        filename = secure_filename(file.filename)
        print(f"Secure filename: {filename}")

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to: {filepath}")

        # Save the file to the upload folder
        file.save(filepath)
        print("File saved successfully.")

        # Validate the Excel file
        print("Starting validation of the file...")
        validation_result = validate_excel(filepath)
        print(f"Validation result: {validation_result}")

        return jsonify(validation_result)

    except Exception as e:
        print("An exception occurred:", str(e))
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure the upload folder exists
    print("Starting Flask server...")
    app.run(debug=True)
