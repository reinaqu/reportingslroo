# -*- coding: utf-8 -*-
import pandas as pd
import dataframes
import commons
from dataclasses import dataclass
from typing import TypeVar, Dict, List, Set
import preconditions
import dois
from builtins import staticmethod, property
from pandas.tests.reshape.test_pivot import dropna

Publications = TypeVar('Publications')


GREY_LITERATURE=["blog", "wiki page", "website", "github", "white paper", "technical report"]
WHITE_LITERATURE=["journal paper", "conference paper", "workshop paper","book chapter","arxiv", "master thesis", "phd thesis", "demo paper"]
WHITE_LITERATURE_LABEL = "White literature"
GREY_LITERATURE_LABEL = "Grey literature"

@dataclass( order=True)
class Publications:
    """

        This class stores all the info about Papers and different Publications written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

        """
    dataframe: pd.DataFrame
    configuration: dict
    citation_df:pd.DataFrame

    @property
    def get_df(self):
        '''
            returns the dataframe we are working with
        '''
        return self.dataframe

    @property
    def get_config(self):
        '''
            returns the configuration we are working with
        '''
        return self.configuration



    @staticmethod
    def of_csv(url: str, config: dict) -> Publications:
        skip_rows= config.get('skip_rows')
        dataframe = pd.read_csv(url, skiprows=skip_rows)
        return Publications(dataframe, config, None)

    @staticmethod
    def of_excel(url: str, config: dict) -> Publications:
        use_cols= config.get('use_cols')
        skip_rows= config.get('skip_rows')
        sheetname=config.get('sheet_name')
        dataframe = pd.read_excel(url, sheet_name=sheetname, skiprows=skip_rows,usecols=use_cols)
        return Publications(dataframe, config, None)
    

    def set_citations_dataframe_from_excel (self, citation_file:str, sheets:List[str])->None:
        dataframe = pd.read_excel(citation_file, sheet_name=sheets[0], usecols=[0,1,6])
        dataframe.rename(columns={"Citations":"Citations-"+sheets[0]}, inplace=True)
        order_list=["Citations-"+sheets[0]]
        for i in range(1,len(sheets)):
            dataframe2 = pd.read_excel(citation_file, sheet_name=sheets[i], usecols=[0,6])
            dataframe2.rename(columns={"Citations":"Citations-"+sheets[i]}, inplace=True)
            dataframe= pd.merge(dataframe, dataframe2, on='ID Paper')
            order_list.append("Citations-"+sheets[i])
        order_list.append('Title')
        ascending_list =[False]*len(sheets)
        ascending_list.append(True)
        print (order_list, ascending_list)    
        dataframe = dataframe\
                    .sort_values(order_list, ascending=ascending_list)\
                    .reset_index(drop=True)
        self.citation_df=dataframe
        
    @property
    def count_studies_by_type(self)->pd.DataFrame:
        preconditions.checkArgument('type' in self.configuration,"Should specify the name of the column for type")
        type_col = self.get_publication_type_colname
        return self.dataframe[type_col]\
                   .dropna()\
                   .astype(str)\
                   .transform(commons.normalize)\
                   .value_counts()\
                   .rename('number of studies',inplace=True)\
                   .rename_axis('type') 

    @property
    def count_studies_by_year(self)->pd.DataFrame:
        preconditions.checkArgument('year' in self.configuration,"Should specify the name of the column for year")
        year_col = self.get_year_colname
        df_studies_by_year= self.dataframe[year_col]\
                                .astype(int)\
                                .value_counts()\
                                .rename('number of studies',inplace=True)\
                                .rename_axis('year') 
        ## As there may be yaars without studies, we must fill the years with zeros
        dataframes.fill_gaps_with_zeros(df_studies_by_year)
       
        return df_studies_by_year.sort_index()

    @property
    def get_ids_title_dois(self)->pd.DataFrame:
        '''
        It returns a dataframe with the id of the paper, the title and its doi
        '''
        preconditions.checkArgument('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument('title' in self.configuration,"Should specify the name of the column for title")
        preconditions.checkArgument('doi' in self.configuration,"Should specify the name of the column for doi")
        id_col = self.get_id_study_colname
        type_col = self.get_doi_colname
        title_col = self.get_title_colname
        #Select only the three columns
        return self.dataframe[[id_col, title_col, type_col]]
    
    @property
    def count_studies_per_datasource(self)->pd.DataFrame:
        '''
        It returns a dataframe with the datasource and the number of studies recovered from that datasource
        '''
        preconditions.checkArgument('id_search' in self.configuration,"Should specify the name of the column for id_search")
        preconditions.checkArgument('searches_datasources' in self.configuration,"Should specify the dictionary with datasources per search")
        id_search_col = self.configuration.get('id_search')
        datasource_per_search = self.configuration.get('searches_datasources')
        res= self.dataframe[id_search_col]\
                    .astype(int)\
                    .apply(datasource_per_search.get)\
                    .value_counts()\
                    .rename('number of studies',inplace=True)\
                    .rename_axis('datasource') 
        return res      
    
    @property
    def get_ordered_studies(self)->pd.DataFrame:
        preconditions.checkArgument('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument('title' in self.configuration,"Should specify the name of the column for title")
        preconditions.checkArgument('year' in self.configuration,"Should specify the name of the column for year")
        preconditions.checkArgument('authors' in self.configuration,"Should specify the name of the column for authors")
        preconditions.checkArgument('publication-type' in self.configuration,"Should specify the name of the column for publication-type")
        preconditions.checkArgument('venue' in self.configuration,"Should specify the name of the column for venue")
         
        id_start_col = self.get_id_study_colname
        title_col = self.get_title_colname
        type_col = self.get_publication_type_colname
        authors_col = self.get_authors_colname      
        venue_col = self.get_venue_colname
        year_col = self.get_year_colname
        
        order_list=[year_col,type_col, title_col]
        filter_list =[id_start_col,title_col, type_col, authors_col,venue_col,year_col]
 
        return self.dataframe[filter_list]\
                   .sort_values(order_list)\
                   .reset_index(drop=True)             
                    
    @property
    def get_id_study_colname(self):
            return self.configuration.get('id_start')
    @property
    def get_title_colname(self):
        return self.configuration.get('title')
    @property
    def get_publication_type_colname(self):    
        return self.configuration.get('publication-type')
    @property
    def get_authors_colname(self):
        return self.configuration.get('authors')       
    @property
    def get_venue_colname(self):
        return self.configuration.get('venue')
    @property
    def get_year_colname(self):
        return self.configuration.get('year')
    @property
    def get_doi_colname(self):
        return self.configuration.get('doi')
    @property
    def get_keywords_dataframe(self)->pd.DataFrame:
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument('keywords' in self.configuration, "Should contain the column for keywords")  
        id_start = self.configuration.get('id_start')
        keywords_col = self.configuration.get('keywords')
        df_column = self.dataframe[[id_start, keywords_col]]\
                        .dropna()  ## To drop empty cells
        return dataframes.create_dataframe_from_multivalued_column(df_column, [id_start,keywords_col], replace_commas=True, transf_function=commons.normalize)
 
    @property
    def get_keywords_per_study(self)->Dict[str,Set[str]]:
        df = self.get_keywords_dataframe
        return dataframes.create_dict_from_single_column(df)