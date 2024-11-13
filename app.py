from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from gradio_client import Client, handle_file
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = Client("niramay/food")

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file extensions
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request."
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file."
        
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Pass the image to the API for classification
            result = client.predict(img=handle_file(image_path), api_name="/predict")

            # Extract prediction details and format output
            label = result['label']
            confidences = result['confidences']
            confidence_text = f"<strong>Prediction:</strong> {label}<br>"
            confidence_text += "<strong>Confidence Scores:</strong><ul>"

            for confidence in confidences:
                confidence_text += f"<li>{confidence['label']}: {confidence['confidence']:.2%}</li>"
            confidence_text += "</ul>"

            # Pass the formatted text to the template
            result = confidence_text
            image_filename = filename

    return render_template('index.html', result=result, image_filename=image_filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
