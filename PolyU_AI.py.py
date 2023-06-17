# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12vbKUlfzn5yJulX9kGGOYD0WdvkJCh8I
"""

import os, sys
from google.colab import drive
drive.mount('/content/drive')

# 컴파일 할 때마다 import 귀찮으니 따로 path 설정
my_path = '/content/notebooks'
os.symlink('/content/drive/MyDrive/Colab Notebooks/pack_env', my_path)
sys.path.insert(0, my_path)

# tomotopy -> 주제 추출
# nltk -> 어근 추출
!pip install --target=$my_path tomotopy
!pip install --target=$my_path nltk

import tomotopy as tp
print(tp.isa)       # 제대로 import 됐는지 확인

import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt')

import nltk
import nltk.stem, nltk.corpus, nltk.tokenize, re
nltk.download('stopwords')

stemmer = nltk.stem.porter.PorterStemmer()
# 영어 단어의 어근만 남겨주는 포터 스테머
stopwords = set(nltk.corpus.stopwords.words('english'))
# 영어 단어의 불용어 집합
rgxWord = re.compile('[a-zA-Z][-_a-zA-Z0-9.]*')
# 특수문자를 제거하기 위해 일반적인 형태의 단어를 나타내는 정규식
# 알파벳으로 시작하고 그 뒤에 알파벳 혹은 숫자, -,_, .가 뒤따라오는 경우만 단어로 취급

# tokenize 함수를 정의
# 문장을 입력하면 단어 단위로 분리하고, 불용어 및 특수 문자 등을 제거한 뒤, 어근만 추출하여 list로 반환
def tokenize(sent):
    def stem(w):
        try: return stemmer.stem(w)
        except: return w

    return [stem(w) for w in nltk.tokenize.word_tokenize(sent.lower()) if w not in stopwords and rgxWord.match(w)]

# 주제 추출하는 변수
mdl = tp.LDAModel(k=1)      # 주제는 상위 하나만 추출(k=1)

# 읽을 파일 가져오기
for line in open('/content/drive/MyDrive/PolyU/news1.txt'):
    mdl.add_doc(tokenize(line))

for i in range(0, 100, 10):
    mdl.train(10)
    print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

for k in range(mdl.k):
    print('Top 10 words of topic #{}'.format(k))
    print(mdl.get_topic_words(k, top_n=10))

mdl.summary()

# 연관성 높은 상위 5개로 주제 추출
mdl.get_topic_words(k, top_n=5)

