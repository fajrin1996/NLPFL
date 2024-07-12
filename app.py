from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, send_from_directory, abort
import os
import pandas as pd
import re
from googletrans import Translator
from normalisasi import correction
import string
from loop_csv import remove_agk, remove_emoj, remove_html, remove_punct, remove_url, \
    remove_stopwords, stemer_word, normalizedterm, detemine
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['DOWNLOAD_FOLDER'] = 'static/download'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

labels = []
scores = []
@app.route('/tampil-hasil/<fileku>', methods=['GET', 'POST'])
def hasil(fileku):
    # nltk.download('punkt')
    # nltk.download('vader_lexicon')
    # dat = SentimentIntensityAnalyzer()

    # try:
    #     return send_from_directory(app.config["DOWNLOAD_FOLDER"], path=fileku, as_attachment=True)

    # except FileNotFoundError:
    #         abort((404))
    read = pd.read_csv('static/download/'+fileku)
    if request.method == "POST":
        read['sentiment']=read['normalisasi'].apply(detemine)
        dt = ['textDisplay', 'sentiment']
        dt = read[dt]
        labeling = dt.to_csv('static/hasil_labeling/hasil_sentiment.csv', columns= ['textDisplay', 'sentiment'])
        return send_from_directory('static/hasil_labeling', path='hasil_sentiment.csv', as_attachment=True, mimetype='csv')
    return render_template('cleansing-data.html', red = read.iterrows())

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
        df['stemmer'] = df['remove_stopwords'].apply(lambda x: stemer_word(x))
        df['normalisasi'] = df['stemmer'].apply(normalizedterm)
        count += 1
        filebaru = df.to_csv('static/download/df_baru'+str(count)+'.csv', index=False)
        return redirect(url_for('hasil', fileku='df_baru'+str(count)+'.csv')) #send_from_directory('static/download', path=filebaru, as_attachment=True, mimetype='csv') #
    else:
        return render_template('tampil_csv.html',table = df.iterrows())

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
