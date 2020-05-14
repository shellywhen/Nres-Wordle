import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
import string
import matplotlib.pyplot as plt
from collections import Counter
with open('stopwords.pkl', 'rb') as f:
    stopwords = pickle.load(f)
def getRawData():
df = pd.read_csv('trump.csv', encoding='utf-8')
df['level']=(df['favorite_count']-df['favorite_count'].mean())/df['favorite_count'].std() + (df['retweet_count']-df['retweet_count'].mean())/df['retweet_count'].std()
df['time'] = pd.to_datetime(df['created_at'],format='%m-%d-%Y %H:%M:%S')
data = df.to_dict(orient='records')
threads = 43781
wordlist = []
paragraph = ""
table = str.maketrans('', '', string.punctuation)
specialWords = ['', '\'', '\"']
for d in data[0:threads]:
    text = d['text'].lower()
    text = re.sub(r"http\S+", '', text)
    atRaw = re.findall(r'@\S*', text)
    ats = [s if s[len(s)-1]!=':' else s[0:-1] for s in atRaw]
    text = re.sub(r'@\S*', '', text)
    time = d['time'].to_pydatetime().strftime('%Y-%m')
    tokens = word_tokenize(text)
    clean_tokens = []
    for token in tokens:
        if token not in stopwords and len(token)>1:
            clean_tokens.append(token)
    fakeSentence = ' '.join(clean_tokens)
    paragraph += fakeSentence
    wordlist.append({'words': clean_tokens, 'level': d['level'], 'time': time, 'ats': ats})
return paragraph, wordlist