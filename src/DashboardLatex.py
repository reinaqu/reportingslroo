'''
Created on 10 jul. 2021

@author: reinaqu_2
'''
import pandas as pd
from dataclasses import dataclass
from typing import TypeVar, List
import Publications as pub
import Venues as ven


DashboardLatex = TypeVar('DashboardLatex')

'''
Dependencies
https://fcache.readthedocs.io/en/stable/

'''


@dataclass(order=True)
class DashboardLatex:
    '''

        This class stores all the info about Papers and different Publications written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

    '''
    publications: pub.Publications
    venues: ven.Venues
    
    @staticmethod   
    def of(publications:pub.Publications) -> DashboardLatex:
        return DashboardLatex(publications,None)
       
    @property
    def get_publications(self) -> pub.Publications:
        return self.publications

    @property
    def get_venues(self) -> ven.Venues:
        return self.venues    
       
    def set_venues(self, venues:ven.Venues)->None:
        self.venues = venues
        
    def generate_citations(self, source_list: List[str])->str:
        
        id_col = self.publications.get_id_study_colname
        title_col = self.publications.get_title_colname
        
        # Generate format string
        format_ini='''{} & \\cite{{{}}} & \\textsf{{{}}}'''
        format_datasource = ''' & {}'''
        end_text =  '''\\\\'''
        
        df = self.publications.citation_df
        for indx, row in df.iterrows():
            ini_text=format_ini.format(indx+1, row[id_col], row[title_col])
            sources_text = ""
            for source in source_list:
                sources_text += format_datasource.format(row ['Citations-'+source])
            print(ini_text+sources_text+end_text)
                
    def generate_studies(self):
        '''
        It prints on the standard output the list of publications in latex format. An example ot the output for a concrete publicacion is the following one:
   
        %S50 id -start: 361084 -------------------------------------------  
        \textsf{S50}  & \cite{conf/atva/AlbertGLRS18} & Peer-to-peer Affine Commitment Using Bitcoin & K. Crary, M. J. Sullivan  & PLDI'15:479-488, 2015\\
        '''
        # %S50 id -start: 361084 -------------------------------------------  
        # \textsf{S50}  & \cite{conf/atva/AlbertGLRS18} & Peer-to-peer Affine Commitment Using Bitcoin & K. Crary, M. J. Sullivan  & PLDI'15:479-488, 2015\\     
        df = self.publications.get_ordered_studies
        id_start_col = self.publications.get_id_study_colname
        title_col = self.publications.get_title_colname
        authors_col = self.publications.get_authors_colname      
        venue_col = self.publications.get_venue_colname
        year_col = self.publications.get_year_colname
        txt='''% id -start: {} -------------------------------------------  
             \\citeS{{{} }} & {} & {} & {},{}\\\\'''

        for _, row in df.iterrows():

            study_id = row[id_start_col]            
            title = row[title_col]
            authors = row[authors_col]
            
            venue = self.venues.get_venue(study_id)
            if venue == None:
                venue = row[venue_col]
            year = row[year_col]
            
            print(txt.format(study_id,study_id,title, authors, venue, year)) 

                