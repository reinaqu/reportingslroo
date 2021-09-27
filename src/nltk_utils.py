# -*- coding: utf-8 -*-
'''
Created on 27 ago. 2021

@author: reinaqu_2
'''

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from typing import List

def tokenizer(keyword:str)->List[str]:
    stemmer = PorterStemmer() #object used to obtain the root of the keywords
    return [stemmer.stem(w) for w in keyword.split()]

def get_stopwords():
    return stopwords.words('english')
