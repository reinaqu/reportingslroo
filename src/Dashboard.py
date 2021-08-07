'''
Created on 10 jul. 2021

@author: reinaqu_2
'''
from dataclasses import dataclass
from typing import TypeVar
import Publications as pub
import graphics_utils as gu
import logging
import Authors as authors

Dashboard = TypeVar('Dashboard')

'''
Dependencies
https://fcache.readthedocs.io/en/stable/

'''

MAP_FILE='../data/countries.geojson'

@dataclass(order=True)
class Dashboard:
    '''

        This class stores all the info about Papers and different Publications written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

    '''
    publications: pub.Publications
    authors:authors.Authors
    
    @staticmethod   
    def of(publications:pub.Publications) -> Dashboard:
        logging.basicConfig(level=logging.INFO)
        return Dashboard(publications, None)
    @property  
    def get_publications(self) -> pub.Publications:
        return self.publications
    
    def set_authors(self, authors:authors.Authors)->None:
        self.authors = authors
        
    @property
    def create_piechart_studies_by_type(self)->None:
        df =self.publications.count_studies_by_type
        gu.create_piechart(df,'number of studies',y_axis_label=False)
    @property
    def create_plot_studies_by_year(self)->None:
        df =self.publications.count_studies_by_year
    #    gu.create_line_plot_multiple_colums(df, 'year', col_names, colours, markers)
        gu.create_lineplot_from_dataframe(df, 'Year', 'Number of studies')
        
    @property
    def create_piechart_studies_by_datasource(self)->None:    
        df = self.publications.count_studies_per_datasource
        gu.create_piechart(df, 'number of studies', y_axis_label=False, font_size=14, label_distance=1.1, pct_distance=0.9)
        
    @property
    def create_map_countries(self)->None:
        df = self.authors.count_number_of_studies_per_country
        gu.create_choropleth_map(df,'number of studies', MAP_FILE)
        