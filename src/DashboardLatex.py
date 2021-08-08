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
import Publications as pub
import Venues as ven
import graphics_utils as gu
from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
from bibtexparser.bparser import BibTexParser
import time
import dois
import logging
import dblp_utils
import json_utils
from tinydb import TinyDB, Query
import db
from pybtex.database import BibliographyData
import bibtex_dblp.database

Dashboard = TypeVar('Dashboard')

'''
Dependencies
https://fcache.readthedocs.io/en/stable/

'''

DBLP_JSON:str="../out/dblp.json"

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
    db:TinyDB
    venues: ven.Venues
    
    @staticmethod   
    def of(publications:pub.Publications) -> Dashboard:
        logging.basicConfig(level=logging.INFO)
        db = TinyDB(DBLP_JSON)
        logging.info("Loading {} documents".format(len(db)))
              
        return DashboardLatex(publications,db,None)
       
    @property
    def get_publications(self) -> pub.Publications:
        return self.publications

    @property
    def get_venues(self) -> ven.Venues:
        return self.venues    
    @property
    def load_db_from_dblp(self)-> None:
        '''
        Load the database with the new documents recovered from dblp.
        '''
        id_col = self.publications.configuration.get('id_start')
        doi_col = self.publications.configuration.get('doi')
        title_col = self.publications.configuration.get('title')
        df = self.publications.get_ids_title_dois
        
        for indx, row in df.iterrows():
            print(indx, row[id_col], row[title_col], row[doi_col])
            id = row[id_col]
            res = db.search_id(self.db, id)
            if res ==None:
                res =dblp_utils.get_bibtext_from_dblp(indx, row[id_col], row[title_col], row[doi_col])
                if res != None:
                    db.insert_dblp(self.db, id, res)
                    
    @property
    def get_authors_dataframe_from_db(self)->pd.DataFrame:
        return db.get_authors_dataframe(self.db)
    
    @property
    def get_venues_dataframe_from_db(self)->pd.DataFrame:
        return db.get_venues_dataframe(self.db)
    
    def set_venues(self, venues:ven.Venues)->None:
        self.venues = venues
        
    def generate_bibtex_from_dblp(self, filename:str)->None:
        dict = db.get_bibtex(self.db)
        bibs = BibliographyData()
        for _, value in dict.items():
            bibs.add_entries(iter(value.entries.items()))
        bibtex_dblp.database.write_to_file(bibs, filename)
        
    
    def generate_cite_from_dblp(self)->str:
        res = ""
        dict = db.get_bibtex(self.db)
        for key, value in dict.items():
            key_list = [key for key,_  in iter(value.entries.items())]
            res+="\\cite{{{}}}\n".format(key_list[0])
        return res    
    
    def generate_citations(self, source_list: List[str])->str:
        txt='''{} & \\textsf{{{}}} & {} & {}\\\\'''
        df = self.publications.citation_df
        for indx, row in df.iterrows():
            print(txt.format(indx+1, row['Title'], row['Citations-GoogleScholar'], row['Citations-Scopus']))
            
    def generate_studies(self):
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
