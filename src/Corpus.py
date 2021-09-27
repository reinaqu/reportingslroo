# -*- coding: utf-8 -*-
'''
Created on 4 sept. 2021

@author: reinaqu_2

dependencies:
    pip install texthero
'''

from dataclasses import dataclass
from typing import TypeVar, Dict, List

import pandas as pd
import texthero as hero
from texthero import preprocessing
import commons

Corpus = TypeVar('Corpus')
V = TypeVar('V')


@dataclass(frozen=True, order=True)
class Corpus:
    
    dataframe: pd.DataFrame
    configuration: Dict[str, V]
    
    @staticmethod
    def of_dataframe(dataframe:pd.DataFrame, config: dict)->Corpus:
        custom_pipeline = [preprocessing.fillna,
                   #preprocessing.lowercase,
                   preprocessing.remove_whitespace,
                   preprocessing.remove_diacritics
                   #preprocessing.remove_brackets
                  ]
        dataframe['clean_abstract'] = hero.clean(dataframe['abstract'], custom_pipeline)
        dataframe['clean_abstract'] = [commons.remove_brackets(n) for n in dataframe['clean_abstract'] ]
        return Corpus (dataframe, config)
    
    
    def get_cleaned_abstracts(self)->List[str]:
        return  self.dataframe['clean_abstract']


        