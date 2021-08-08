'''
Created on 10 jul. 2021

@author: reinaqu_2
'''
import pandas as pd
from csvbib_utils import *
import dataframes
import csv
from dataclasses import dataclass
from typing import TypeVar
import DataExtraction as datext
import graphics_utils as gu
from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
from bibtexparser.bparser import BibTexParser
import time
import dois
import logging
from fcache.cache import FileCache
import dblp_utils
import json_utils

DashboardDataExtraction = TypeVar('DashboardDataExtraction')
K = TypeVar('K')
V = TypeVar('V')
E = TypeVar('E')
'''
Dependencies
https://fcache.readthedocs.io/en/stable/

'''

@dataclass(frozen=True, order=True)
class DashboardDataExtraction:
    '''

        This class stores all the info about Papers and different Publications written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

    '''
    data: datext.DataExtraction
    
    @staticmethod   
    def of(data:datext.DataExtraction) -> DashboardDataExtraction:
        logging.basicConfig(level=logging.INFO)
        return DashboardDataExtraction(data)
    @property  
    def get_data(self) -> datext.DataExtraction:
        return self.data

        
    
    def create_piechart_count_multivalued_column(self, column_name:str, exclude:List[E])->None:    
        serie_count = self.data.count_multivalued_column(column_name)
        serie_count = dataframes.exclude_index_values_from_series(serie_count, exclude)
        gu.create_piechart(serie_count, column_name, y_axis_label=False, font_size=14, label_distance=1.1, pct_distance=0.9)
    
    def create_bar_count_multivalued_column(self, column_name:str, rotation:int=90, translation:Dict[K,V]={}, exclude:List[K]=[])->None:    
        count_serie = self.data.count_multivalued_column(column_name)
        count_serie =  dataframes.exclude_index_values_from_series(count_serie, exclude)
            
        if len(translation) > 0:
            count_serie = dataframes.translate_index_dataframe (count_serie,translation)
        gu.create_bar(count_serie,x_labels_rotation=rotation)
     

    
    def create_bubble(self, facet1_name:str, facet2_name:str):
        df_count = self.data.count_faceted_multivalued_column(facet1_name, facet2_name)
        gu.create_bubble(df_count, 'number of studies', facet1_name, facet2_name)