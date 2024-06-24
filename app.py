from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pandas as pd
import csv
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file-csv/<nama>')
def tampil_csv(nama):
    result = []
    df = pd.read_csv('static/upload/'+nama)
    return render_template('tampil_csv.html',table = [df.to_html()] , title=[''])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(filename)
        return redirect(url_for('tampil_csv',nama=filename))


if __name__ == '__main__':
    app.run(debug=True)
