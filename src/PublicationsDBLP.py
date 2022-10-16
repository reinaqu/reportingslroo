'''
Created on 10 jul. 2021

@author: reinaqu_2
'''
import pandas as pd
from dataclasses import dataclass
from typing import TypeVar, List
import Publications as pub
import Venues as ven
import logging
import dblp_utils
from tinydb import TinyDB
import db
from pybtex.database import BibliographyData
import bibtex_dblp.database

PublicationsDBLP = TypeVar('PublicationsDBLP')

'''
Dependencies
https://fcache.readthedocs.io/en/stable/

'''

DBLP_JSON:str="../out/dblp.json"

@dataclass(order=True)
class PublicationsDBLP:
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
    def of(publications:pub.Publications) -> PublicationsDBLP:
        logging.basicConfig(level=logging.INFO)
        db = TinyDB(DBLP_JSON)
        logging.info("Loading {} documents".format(len(db)))
              
        return PublicationsDBLP(publications,db,None)
       
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
        id_col =self.publications.get_id_study_colname
        doi_col = self.publications.get_doi_colname
        title_col = self.publications.get_title_colname
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
    

