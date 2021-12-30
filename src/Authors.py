# -*- coding: utf-8 -*-
'''
@author: Toñi Reina Quintero
'''
import pandas as pd
import dataframes
from dataclasses import dataclass
from typing import TypeVar, Dict
import preconditions
from collections import defaultdict
from sortedcontainers.sortedset import SortedSet


Authors = TypeVar('Authors')
K = TypeVar('K')
V = TypeVar('V')


@dataclass(frozen=True, order=True)
class Authors:
    """

        This class stores all the info about Authors  written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe obtained from the csv or Excel sheet.
            2. Configuration: stores a Dict which pair key-value are the different values of configuration


    """
    dataframe: pd.DataFrame
    configuration: Dict [K,V]

    @property
    def get_df(self)->pd.DataFrame:
        '''
            @return: the dataframe we are working with that stores all the author information
        '''
        return self.dataframe

    @property
    def get_config(self)->Dict [K,V]:
        '''
            @return: the configuration we are working with
        '''
        return self.configuration


    @staticmethod
    def of_dataframe(dataframe:pd.DataFrame, config: Dict [K,V])->Authors:
        '''
        @param dataframe: dataframe with the authors data.
        @param config: Dictionary with the configuration of the dataframe.
        @return An authors object composed of the dataframe and the configuration dictionary given as parameters.
        '''
        return Authors (dataframe, config)
    
    @staticmethod
    def of_csv(filename: str, config: Dict [K,V], separator:str=',') -> Authors:
        '''
        @param filename: filename (and path) of the csv file with data.
        @param config: Dictionary with the configuration.
        @param separator: Separator used in the csv file to separate data.
        @return An authors object composed of the dataframe created with the csv data and the configuration dictionary given as parameters.
        '''
        skip_rows= config.get('skip_rows')
        dataframe = pd.read_csv(filename, skiprows=skip_rows, sep=separator)
        return Authors(dataframe, config)

    @staticmethod
    def of_excel(filename: str, config: Dict [K,V]) -> Authors:
        '''
        @param filename: filename (and path) of the Excel sheet with data.
        @param config: Dictionary with the configuration.
        @param separator: Separator used in the csv file to separate data.
        @return An authors object composed of the dataframe created with the Excel file data and the configuration dictionary given as parameters.
        @invariant: The configuration dictionary should have a key 'use_cols' with the numbers of the columns of the Excel file 
        that are going to be used to create the dataframe.
        @invariant: The configuration dictionary should have a key 'skip_rows' with the numbers of skipped rows of the Excel file 
        that are going to be used to create the dataframe.
        @invariant: The configuration dictionary should have a key 'sheet_name' with the name of the sheet of the Excel file 
        that hold data to be used to create the dataframe.
        '''
        use_cols= config.get('use_cols',None)
        skip_rows= config.get('skip_rows',None)
        sheetname=config.get('sheet_name',None)
        dataframe = pd.read_excel(filename, sheet_name=sheetname, skiprows=skip_rows,usecols=use_cols)
        return Authors(dataframe, config)

    
    @property
    def get_count_col(self):
        '''
        @return: the name of the column of the dataframes that group and count certain properties.
        '''
        return 'number of studies'
    
    @property
    def get_author_name_col(self):
        '''
        @return: the name of the column of the dataframes given to the author name. Note that the name of this column is 
        configurable and depends on the name given to this column in the original datasource.
        '''
        return self.get_config.get('author_name')
    
    @property
    def count_number_of_studies_per_author(self)->pd.DataFrame:
        '''
        @return: a dataframe with two columns; one with the author name, and another one with the number of studies published
        by that author. An example of the resulting dataframe is:
                Author name  number of studies
        0     Mathias Weske                 12
        1    Anne Baumgrass                  9
        2        Hyerim Bae                  6
        3      Jan Mendling                  6
        4       Martin Roth                  6
        @invariant: The configuration dictionary should have a key 'author_ID' with the name of the column that holds 
        the id of the authors used in the original dataframe.
        @invariant: The configuration dictionary should have a key 'author_name' with the name of the column that holds 
        the name of the authors used in the original dataframe.
        '''
        preconditions.checkArgument('author_ID' in self.configuration,"Should specify the name of the column for author id")
        preconditions.checkArgument('author_name' in self.configuration,"Should specify the name of the column for author name")
        authorid_col = self.configuration.get('author_ID')
        authorname_col = self.configuration.get('author_name')
       
        #create two dictionaries to group by author_id, one with the count (d_count) and  the other one with
        #the names of the authors (d_name) this last one is needed because the same author could appear with different names
        #the majority of the author ids have been obtained from dblp
        d_count = defaultdict(int)  # {author-id:number of studies} ==>{str:int} 
        d_names = defaultdict(SortedSet) # {author-id:SortedSet with author names} ==>{str:SortedSet(str)}
        for _, row in self.dataframe.iterrows():
            authorID = row[authorid_col]
            authorname = row[authorname_col]
            d_count[authorID]+=1
            d_names[authorID].add(authorname)
            
        #Make a third dict with authors names as keys and counts as values. If one author has various names, we use 
        #the first one
        d_names_count ={(d_names.get(authorid).pop(0), count) for authorid, count in d_count.items()}       
        #sort the dict by value/count (descending), and then by key/name (ascending)            
        sorted_count = sorted(d_names_count,key=lambda t:(-t[1],t[0]))
        names, counts = zip(*sorted_count)
        return pd.DataFrame(data={authorname_col: names,
                                 'number of studies': counts})

    
    
    @property
    def count_number_of_studies_per_country(self)->pd.DataFrame:        
        '''
        @return: a dataframe with two columns; one with the country name, and another one with the number of studies published
        by that authors of that country. An example of the resulting dataframe is:
              countries    number of studies
            0 Germany        64
            1 South Korea    16
            2 Austria        14
            3 Netherlands    13
            4 Italy          13
        @invariant: The configuration dictionary should have a key 'id_start' with the name of the column that holds 
        the id of study used in the original dataframe.
        @invariant: The configuration dictionary should have a key 'country' with the name of the column that holds 
        the name of the country used in the original dataframe.
        '''
        #check the configuration has the columns we need
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkState('country' in self.configuration,"Should specify the name of the column for country")
        #get the column names from the configuration
        id_start = self.configuration.get('id_start')
        country_col = self.configuration.get('country')  
        #create the dataframe with the id of the study and the country
        df_column = self.dataframe[[id_start, country_col]]    
        #create a dictionary {country: Set(id_study)} ==> {str:Set(str)} (dict_countries)
        dict_countries = dataframes.create_dict_from_multivalued_column(df_column)
        #create a dictionary {id_study: int} that relates a study and the number of different countries that participate in that study
        dict_count = {id_study:len(ss) for id_study, ss in dict_countries.items()}
        #sort the dictionary by the number of countries descending
        count_sorted =sorted(dict_count.items(), key=lambda t:t[1], reverse=True)
        names, counts = zip(*count_sorted)
        return pd.DataFrame(data={'countries': names,
                                 'number of studies': counts})

