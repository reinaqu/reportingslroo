'''
Created on 10 jul. 2021

@author: reinaqu_2
'''
import pandas as pd
from dataclasses import dataclass
from typing import TypeVar, List
import Publications as pub
import Venues as ven
import Authors as aut


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
    authors: aut.Authors
    
    @staticmethod   
    def of(publications:pub.Publications) -> DashboardLatex:
        return DashboardLatex(publications,None, None)
       
    @property
    def get_publications(self) -> pub.Publications:
        return self.publications

    @property
    def get_venues(self) -> ven.Venues:
        return self.venues    

    @property
    def get_authors(self) -> aut.Authors:
        return self.authors    
           
    def set_venues(self, venues:ven.Venues)->None:
        self.venues = venues

    def set_authors(self, authors:aut.Authors)->None:
        self.authors = authors
        
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

    def generate_authors(self):            
        
        '''
        It prints on the standard output the list of authors and their number of publications in latex format.
         An example ot the output for a concrete author is the following one:
   
        Mathias Weske       & 12\\
        '''
        df = self.authors.count_number_of_studies_per_author
 
        for _, row in df.iterrows():
            author_name_col = self.get_authors.get_author_name_col
            count_col = self.get_authors.get_count_col
            author = row[author_name_col]            
            count = row[count_col]
            
            print(f"{author} & {count} \\\\ ") 
    
    def generate_venues(self):
        df = self.get_venues.count_number_of_studies_per_venue
        rank = 1
        for _, row in df.iterrows():
            venue_name_col = self.get_venues.get_venues_name_col
            type_name_col = self.get_venues.get_type_name_col
            count_col = self.get_venues.get_count_col
            venue = row[venue_name_col]
            type = row[type_name_col]
            number = row [count_col]   
            print(f"{rank} & {venue} & {type} & {number} \\\\ ") 
            rank+=1