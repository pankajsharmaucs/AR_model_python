from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directory for uploaded images
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']

        # If the user does not select a file, the browser also
        # submit an empty part without filename
        if file.filename == '':
            return "No selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the image
            processed_filename = process_image(filepath)
            return redirect(url_for('display_image', filename=processed_filename))
    
    return render_template('index.html')

def process_image(filepath):
    # Read the image using OpenCV
    image = cv2.imread(filepath)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the processed image
    processed_filename = 'output.jpg'
    processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
    cv2.imwrite(processed_filepath, gray)

    return processed_filename

@app.route('/display/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
