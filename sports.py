import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import *
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

from xgboost import XGBClassifier, XGBRegressor

import re
import nltk
from string import punctuation

def preprocessa(txt):

    numbers = '0123456789'
    stopwords = nltk.corpus.stopwords.words('portuguese')

    txt = txt.lower()
    txt = ''.join([c for c in txt if c not in punctuation + numbers])
    txt = re.sub(r'\n|\r', '', txt)
    txt = re.sub(r' .+? ', ' ', txt)
    txt = ' '.join([t for t in txt.split(' ') if t not in stopwords])

    return txt

model = XGBClassifier(
    n_estimators=120,
    max_depth=3,
    n_jobs=-1,
    random_state=1
)

df = pd.read_csv('noticias.csv')
tfidf_vectorizer = TfidfVectorizer()

def treina():
    df['noticia'] = df['noticia'].apply(preprocessa)

    tfidf_matrix = tfidf_vectorizer.fit_transform(df['noticia'])

    model.fit(
        tfidf_matrix, df['target']
    )

treina()

def testa(noticia):
    df_teste = pd.DataFrame([preprocessa(noticia)], columns=['noticia'])
    tfidf_matrix = tfidf_vectorizer.transform(df_teste['noticia'])
    proba = model.predict_proba(tfidf_matrix)[:,1]
    return float(proba[0])
