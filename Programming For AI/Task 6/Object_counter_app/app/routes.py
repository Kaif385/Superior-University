from flask import render_template, request
import os
from app import app
from app.camera import detect_animals

@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            result_text = "No file part"
            return render_template('index.html', result=result_text)
        
        file = request.files['file']
        if file.filename == '':
            result_text = "No selected file"
            return render_template('index.html', result=result_text)

        upload_folder = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        upload_path = os.path.join(upload_folder, file.filename)
        file.save(upload_path)

        result_text, marked_image_path = detect_animals(upload_path)
        print("Detection Result:", result_text)


        output_path = os.path.join(os.getcwd(), 'detection_result.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result_text)

        return render_template('index.html', result=result_text, filename="marked_" + file.filename)

    return render_template('index.html', result=result_text)
from flask import send_from_directory

