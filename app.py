from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pandas as pd

import re
import string
from loop_csv import remove_agk, remove_emoj, remove_html, remove_punct, remove_url, remove_stopwords

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/file-csv/<nama>', methods=['GET', 'POST'])
def tampil_csv(nama):
    count = 0
    df = pd.read_csv('static/upload/'+nama)
    if request.method == 'POST':
        df = pd.DataFrame(df['textDisplay'])
        df
        df['cleansing'] = df['textDisplay'].apply(lambda x: remove_url(x))
        df['cleansing'] = df['cleansing'].apply(lambda x: remove_html(x))
        df['cleansing'] = df['cleansing'].apply(lambda x: remove_emoj(x))
        df['cleansing'] = df['cleansing'].apply(lambda x: remove_agk(x))
        df['cleansing'] = df['cleansing'].apply(lambda x: remove_punct(x))
        df['tokenz_and_caseFold'] = df['cleansing'].apply(lambda x: x.lower().split())
        df['remove_stopwords'] = df['tokenz_and_caseFold'].apply(lambda x: remove_stopwords(x))
        count += 1
        # filebaru = 
        return redirect(url_for('hasil',fileku=df.to_csv('df_baru'+str(count)+'.csv', index=False)))
    else:
        return render_template('tampil_csv.html',table = df.iterrows())

@app.route('/tampil-hasil/<fileku>')
def hasil(fileku):
    read = pd.read_csv(fileku)
    return render_template('cleansing-data.html', red = read.iterrows())

@app.route('/upload', methods=['GET', 'POST'])
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


    
    

        
        

        df

if __name__ == '__main__':
    app.run(debug=True)
