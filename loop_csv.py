import pandas as pd 
import re
import string
from nltk.corpus import stopwords
import nltk
from googletrans import Translator

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
nltk.download('stopwords')
stop_words = stopwords.words('indonesian')
# stop_words.extend('sm', 'yg', 'otake')

# data = pd.read_csv('/home/rins/web-development/NLP/static/upload/youtube-comments.csv')

# for di, dt in data.iterrows():
#     print(dt['authorDisplayName'])
def remove_url(tweet):
        url = re.compile(r'https?://\S|www\. \S+')
        return url.sub(r'', tweet)

def remove_html(tweet):
        html = re.compile(r'<.*?>')
        return html.sub(r'', tweet)

def remove_emoj(tweet):
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F" # emoticons
                                u"\U0001F300-\U0001F5FF" # symbols & pictographs
                                u"\U0001F680-\U0001F6FF" # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF" # flags (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', tweet)

def remove_agk(tweet):
        tweet = re.sub('[0-9]+', '', tweet)
        tweet = re.sub(r'\$\W*', '', tweet)
        tweet = re.sub(r'^RT[\s]', '', tweet)
        tweet = re.sub(r'#', '', tweet)
        return tweet
def remove_punct(tweets):
        translator = str.maketrans('', '', string.punctuation)
        return tweets.translate(translator)

def remove_stopwords(text):
  return [word for word in text if word not in stop_words]

def stemer_word(text):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
       
        return [stemmer.stem(word) for word in text]

def translate_tweet(tweet, target_language='en'):
       translator = Translator()
       translation = translator.translate(tweet, dest=target_language)
       return translation.text