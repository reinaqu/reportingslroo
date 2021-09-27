# -*- coding: utf-8 -*-
'''
Created on 16 ago. 2021

@author: reinaqu_2

Notes:
Dependencies
- pandas
- numpy
- nltk (natural language toolkit)
  pip install nltk
- sklearn  (clus)
  pip install sklearn
'''

import pandas as pd
import numpy as np



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster

from dataclasses import dataclass
from typing import TypeVar, Dict, List, Set
from sklearn.cluster._affinity_propagation import AffinityPropagation
import nltk_utils as nlut

KeywordClusterer = TypeVar('KeywordClusterer')

@dataclass( order=True)
class KeywordClusterer:
    affinity_propagation : AffinityPropagation #object that executes the clustering affinity propagation algorithm
    keywords:List[str] #list of keywords
    tfidf: TfidfVectorizer #object that converts the keywords to numbers
    X: pd.DataFrame #dataframe with numbers obtained from keywords
    @staticmethod
    def of(keywords:List[str]) -> KeywordClusterer:           
        keywords =keywords
        affinity_propagation = cluster.AffinityPropagation(verbose=True, damping=0.9, max_iter=2000, convergence_iter=200)
        tfidf = TfidfVectorizer(tokenizer=nlut.tokenizer, stop_words=nlut.get_stopwords())
        #tfidf.fit_transform(self.keywords).toarray() converts the keywords
        #to an array of numbers. To apply the clustering algorithm we need to
        #covert text to numbers
        X = pd.DataFrame(tfidf.fit_transform(keywords).toarray(),
                 index=keywords, columns=tfidf.get_feature_names())
        
        return KeywordClusterer (affinity_propagation, keywords, tfidf, X)




    def predict(self)->np.ndarray:
        return self.affinity_propagation.fit_predict(self.X)
    
    @property
    def get_number_of_clusters(self)->int:
        return len(self.affinity_propagation.cluster_centers_indices_)
    
    @property
    def get_labels(self)->np.ndarray:
        return self.affinity_propagation.labels_
    
    @property
    def get_X(self)->pd.DataFrame:
        return self.X
    
    def get_prediction(self)->pd.DataFrame:
        return pd.DataFrame(self.predict(),
                 index=self.keywords, columns=['cluster'])
        