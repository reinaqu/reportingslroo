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
import preconditions

Dashboard = TypeVar('Dashboard')

'''
Dependencies
https://fcache.readthedocs.io/en/stable/

'''



@dataclass(order=True)
class Dashboard:
    '''

        This class represents a dashboard that holds all the operations that can be executed with data related to the publications
        themselves. That is, operatations that are common to every sytematic literature review and that do not depend on the
        specific domain of the review.

        The class has three attributes:
            1. publications: stores the object that holds the set of publications that are reviewed.
            2. authors: stores the object that holds the set of authors of the publications that are reviewed.
            3. geojson_file: filename (with path) of the geojson file with the geolocalized countries to draw a mep with the
            geolocalized studies.
    '''
    publications: pub.Publications
    authors:authors.Authors
    geojson_file:str
    
    @staticmethod   
    def of(publications:pub.Publications) -> Dashboard:
        '''
        @param publications: the object that holds the set of publications that are reviewed.
        @return: A Dashboard object with the publications initialized and with no authors information nor geojson file.
        '''
        logging.basicConfig(level=logging.INFO)
        return Dashboard(publications, None, None)
    
    @property  
    def get_publications(self) -> pub.Publications:
        '''
        @return: the object that holds the set of publications that are reviewed.
        '''
        return self.publications
    
    def set_authors(self, authors:authors.Authors)->None:
        '''
        @param authors:  object that holds the set of authors of the publications that are reviewed.
        It sets the authors.
        '''
        self.authors = authors

    def set_geojson_file(self, geojson_file:str)->None:
        '''
        @param geojson_file: filename (with path) of the geojson file with the geolocalized countries to draw a mep with the
            geolocalized studies.
        '''
        self.geojson_file = geojson_file
        
    @property
    def create_piechart_studies_by_type(self)->None:
        '''
        It draws a piechart with the studies by type of publication (conference, workwhops, journal, ...)
        '''
        df =self.publications.count_studies_by_type
        #font_size=9, label_distance=1.1, pct_distance=0.8,radius=1)
        gu.create_piechart(df,'number of studies',y_axis_label=False, font_size=12, label_distance=1.2, pct_distance=1.1)
        
    @property
    def create_plot_studies_by_year(self)->None:
        '''
        It draws a line plot chart with the studies by year
        '''
        df =self.publications.count_studies_by_year
    #    gu.create_line_plot_multiple_colums(df, 'year', col_names, colours, markers)
        gu.create_lineplot_from_dataframe(df, 'Year', 'Number of studies')
        
    @property
    def create_piechart_studies_by_datasource(self)->None:    
        '''
        It draws a pie chart chart with the studies by datasource (ACM, IEEE, Google Scholar, ....)
        '''
        df = self.publications.count_studies_per_datasource
        gu.create_piechart(df, 'number of studies', y_axis_label=False, font_size=12, label_distance=1.2, pct_distance=1.1)
        
    @property
    def create_map_countries(self)->None:
        '''
        @invariant: The geojson file with the coordinates of the countries should be hold in the corresponding attribute.
        It draws a map that represents the number of studies per country. Tbe calculation is done having into account the
        country of the authors of the studies. The country of an author is determined by the institution she belongs to. Thus,
        one study is map to the different countries of their authors.
        '''
        preconditions.checkState(self.geojson_file!=None, "The file with the coordinates of countries should be set")
        df = self.authors.count_number_of_studies_per_country
        gu.create_choropleth_map(df,'number of studies', self.geojson_file)
        