'''
Created on 10 jul. 2021

@author: reinaqu_2
'''
import pandas as pd
import dataframes
from dataclasses import dataclass
from typing import TypeVar,List,Dict, Set
import DataExtraction as datext
import PublicationsQuality as pubq
import graphics_utils as gu
import logging
from lxml import includes


DashboardDataExtraction = TypeVar('DashboardDataExtraction')
K = TypeVar('K')
V = TypeVar('V')
E = TypeVar('E')
'''
Dependencies
https://fcache.readthedocs.io/en/stable/

'''

@dataclass( order=True)
class DashboardDataExtraction:
    '''

        This class stores all the info about Papers and different Publications written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

    '''
    data: datext.DataExtraction
    pub_quality: pubq.PublicationsQuality
    
    @staticmethod   
    def of(data:datext.DataExtraction) -> DashboardDataExtraction:
        logging.basicConfig(level=logging.INFO)
        return DashboardDataExtraction(data, None)
    
    @property  
    def get_data(self) -> datext.DataExtraction:
        return self.data

    @property  
    def get_publications_quality(self) -> datext.DataExtraction:
        return self.pub_quality

    def set_publications_quality(self, pub_quality: pubq.PublicationsQuality):
        self.pub_quality = pub_quality
    
    def create_piechart_count_multivalued_column(self, column_name:str, translation:Dict[K,V]={}, exclude:List[E]=[])->None:    
        count_serie = self.data.count_multivalued_column(column_name)  
        count_serie =  dataframes.exclude_index_values_from_series(count_serie, exclude)
        if len(translation) > 0:
            count_serie = dataframes.translate_index_dataframe (count_serie,translation)
            
        gu.create_piechart(count_serie, 'number of studies', y_axis_label=False, font_size=14, label_distance=1.1, pct_distance=0.8)
    
    def create_bar_count_multivalued_column(self, column_name:str, rotation:int=90, translation:Dict[K,V]={}, exclude:List[K]=[])->None:    
        count_serie = self.data.count_multivalued_column(column_name)
        count_serie =  dataframes.exclude_index_values_from_series(count_serie, exclude)
            
        if len(translation) > 0:
            count_serie = dataframes.translate_index_dataframe (count_serie,translation)
        gu.create_bar(count_serie,x_labels_rotation=rotation)
  
    def create_bar_count_faceted_multivalued_column_filtered(self, facet1_name:str, facet2_name:str, include:Set[str], rotation:int=90, translation:Dict[K,V]={}, exclude:List[K]=[])->None:    
        count_serie = self.data.count_faceted_multivalued_column_filtered(facet1_name, facet2_name, include)
        count_serie =  dataframes.exclude_index_values_from_series(count_serie, exclude)
            
        if len(translation) > 0:
            count_serie = dataframes.translate_index_dataframe (count_serie,translation)
        gu.create_bar(count_serie,x_labels_rotation=rotation)   

    def create_bar_count_single_column_with_multiple_values(self, column_name:str, rotation:int=90, translation:Dict[K,V]={}, exclude:List[K]=[], count_inferior_limit:int=None)->None:    
        count_serie = self.data.count_single_column_with_multiple_values(column_name)
        if count_inferior_limit != None:
            count_serie = count_serie [count_serie > count_inferior_limit]
        
        count_serie =  dataframes.exclude_index_values_from_series(count_serie, exclude)
            
        if len(translation) > 0:
            count_serie = dataframes.translate_index_dataframe (count_serie,translation)
        gu.create_bar(count_serie,x_labels_rotation=rotation)
        
    def create_bubble(self, facet1_name:str, facet2_name:str):
        df_count = self.data.count_faceted_multivalued_column(facet1_name, facet2_name)
        gu.create_bubble(df_count, 'number of studies', facet1_name, facet2_name)
    
    def create_bubble_filled_with_default(self, facet1_name:str, facet2_name:str, include:Set[str],default_facet2_value:str='n/a'):        
        df_count = self.data.count_faceted_multivalued_column_filled_with_default(facet1_name, facet2_name, include, default_facet2_value)
        gu.create_bubble(df_count, 'number of studies', facet1_name, facet2_name)
        
    def create_bubble_quality(self):
        '''
        It generates a bubble plot with intrinsiq IQ ( X-axis) and contextual IQ (Y-axis)
        data. 
        '''
        df_count = self.get_publications_quality.count_pairs_per_quality_measure
        intr_iq_colname =self.get_publications_quality.get_intrinsic_iq_colname
        cont_iq_colname = self.get_publications_quality.get_contextual_iq_colname
        #As there are pairs of values that are not present in the dataframe,
        #we need to set up labels
        labels =['LOW', 'MEDIUM', 'HIGH']
        gu.create_bubble(df_count, 'number of studies', intr_iq_colname, cont_iq_colname,\
                          rows=labels, columns=labels)    
            
       
    def create_bubble_multivalued_single(self, multivalued_column:str, single_column:str, include:List[str]):
        df_count = self.get_data.count_faceted_multivalued_single_column_filtered(multivalued_column, single_column,set(include))
        rows_labels = include
        column_labels = self.get_data.get_single_column_values(single_column)
        single_column = self.get_data.get_config.get(single_column)
        gu.create_bubble2(df_count, 'number of studies', single_column, multivalued_column)
        
    def create_dict_from_multivalued_column(self, column_name: str)->Dict[str, Set[str]]:
        '''
        @param column_name: Name of the column used to generate the dictionary
        @return: A dictionary in which the keys are the different values of the multivalued column and the values
        are sets with the ids of the studies that have that value.
        '''
        return self.get_data.create_grouping_dict_from_multivalued_colum(column_name)
#     def create_line_plot_multivalued_single(self, multivalued_column:str, single_column:str, include:List[str]):
#       df_count = self.get_data.count_faceted_multivalued_single_column_filtered(multivalued_column, single_column,set(include))
#       col_names=['process redesign','process monitoring', 'process implementation', 'process identification', 'process discovery', 'process analysis']
#       colours =['orange','grey', 'red', 'green', 'blue', 'pink']
#       markers =[gu.MARKER_SQUARE,gu.MARKER_CIRCLE,gu.MARKER_SQUARE,gu.MARKER_CIRCLE, gu.MARKER_SQUARE,gu.MARKER_CIRCLE]
#       print(df_count)
#       single_column =self.get_data.get_config.get(single_column)
#       gu.create_line_plot_multiple_colums(df_count,single_column, col_names, colours ,markers)