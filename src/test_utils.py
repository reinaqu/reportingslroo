'''
Created on 28 nov. 2021

@author: reinaqu_2
'''
import configurations
import DashboardDataExtraction as datextdash
import PublicationsQuality as pubq

from typing import TypeVar,Callable,Dict,List, Set
K = TypeVar('K')
V = TypeVar('V')



def show_dict(d: Dict[str, Set[str]]):
    ## sorted by number of elements of the set (descending) and the key, ascending
    ordered = sorted(d.items(), key=lambda it:(-len(it[1]), it[0]))
    for k,v in sorted(ordered, reverse=True):
        print (k, '-->', list(v))
        
def show_dict_latex(d:Dict[str,Set[str]]):
    ## sorted by number of elements of the set (descending) and the key, ascending
    ordered = sorted(d.items(), key=lambda it:(-len(it[1]), it[0]))
    for key, value in ordered:
        str_value = ", ".join(map(lambda s:f"\cite{{{s:}}}", value))
        print(f"{key}\n\t{str_value}") 

def show_quality_bubble_plot(quality_file:str, datadash:datextdash.DashboardDataExtraction):
    pub_quality = pubq.PublicationsQuality.of_excel(quality_file, configurations.config_publ)  
    datadash.set_publications_quality(pub_quality)
    #print(pub_quality.count_pairs_per_quality_measure)
    datadash.create_bubble_quality() 
    
def show_dict_from_multivalued_column(datadash:datextdash.DashboardDataExtraction, column_name: str):
    d =datadash.create_dict_from_multivalued_column(column_name)
    show_dict(d)

def show_dict_latex_from_multivalued_column(datadash:datextdash.DashboardDataExtraction, column_name: str):
    d =datadash.create_dict_from_multivalued_column(column_name)
    show_dict_latex(d)        
    
def show_dict_latex_from_single_column(datadash:datextdash.DashboardDataExtraction, column_name: str):
    d =datadash.create_dict_from_single_column(column_name)
    show_dict_latex(d)        