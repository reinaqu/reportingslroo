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



def mostrar_dict(d: Dict[str, Set[str]]):
     for k,v in sorted(d.items()):
        print (k, '-->', list(v))

def show_quality_bubble_plot(quality_file:str, datadash:datextdash.DashboardDataExtraction):
    pub_quality = pubq.PublicationsQuality.of_excel(quality_file, configurations.config_publ)  
    datadash.set_publications_quality(pub_quality)
    print(pub_quality.count_pairs_per_quality_measure)
    datadash.create_bubble_quality()
    
    
def show_dict_from_multivalued_column(datadash:datextdash.DashboardDataExtraction, column_name: str):
    d =datadash.create_dict_from_multivalued_column(column_name)
    mostrar_dict(d)
        