import pandas as pd 
import re
import string
from nltk.corpus import stopwords
import nltk
from googletrans import Translator
from deep_translator import MyMemoryTranslator
import csv
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
nltk.download('stopwords')
stop_words = stopwords.words('indonesian')
stop_words.extend(['sm', 'yg', 'mka', 'tdk', 'mk', 'klo', 'amp', 'bikin', 'bkn', 'gk', 'gak', 'jgn', 'ga'
                   'sih', 'nih', 'nya', 'utk' ])

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
       translator = MyMemoryTranslator(source='id-ID', target='en-GB').translate(tweet, return_all=False)
       
       return translator

kamus_data = pd.read_excel('static/kamuskatabaku.xlsx')
normalized_word_dict = {}
for ind, row in kamus_data.iterrows():
       if row[0] not in normalized_word_dict:
              normalized_word_dict[row[0]] = row[1]

def normalizedterm(document):
       return [normalized_word_dict[term] if term in normalized_word_dict else term for term in document]

pos_lex = set(pd.read_csv('static/positive_t.tsv', sep='\t', header=None)[0])
lex_neg = set(pd.read_csv('static/negative_t.tsv', sep='\t', header=None)[0])



def detemine(tweet):
       pos_count = sum(1 for word in tweet if word in pos_lex)

       neg_count = sum(1 for word in tweet if word in lex_neg)
       if pos_count > neg_count:
              return 'Positive'
       elif pos_count < neg_count:
              return "Negative"
       else: 
              return "Netral"
'''
lexicon_pos = dict()
with open('static/positive.txt','r') as csvfile:
       reader = csv.reader(csvfile, delimiter=',')
       for row in reader:
             lexicon_pos[row[0]] = row[1] 


lexicon_neg = dict()
with open('static/negative.txt','r') as csvfile:
       reader = csv.reader(csvfile, delimiter=',')
       for row in reader:
             lexicon_neg[row[0]] = row[1] 
        
def sentiment_anal(tweet):
       score = 0
       for word in tweet:
              if word in lexicon_pos:
                     score = score + lexicon_pos[word]

       for word in tweet:
              if word in lexicon_neg:
                     score = score + lexicon_neg[word]
       polarity = ''
       if score > 0:
              polarity = 'Positiv'

       if  score > 0:
              polarity = 'Negative'
       else: 
              polarity = 'neutral'

       return polarity 
             
'''