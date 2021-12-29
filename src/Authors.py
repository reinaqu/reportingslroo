# -*- coding: utf-8 -*-
import pandas as pd
import dataframes
from dataclasses import dataclass
from typing import TypeVar
import preconditions
from collections import defaultdict
from sortedcontainers.sortedset import SortedSet


Authors = TypeVar('Authors')



@dataclass(frozen=True, order=True)
class Authors:
    """

        This class stores all the info about Authors and different written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration


    """
    dataframe: pd.DataFrame
    configuration: dict

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
    def of_dataframe(dataframe:pd.DataFrame, config: dict)->Authors:
        return Authors (dataframe, config)
    @staticmethod
    def of_csv(url: str, config: dict, separator=',') -> Authors:
        skip_rows= config.get('skip_rows')
        dataframe = pd.read_csv(url, skiprows=skip_rows, sep=separator)
        return Authors(dataframe, config)

    @staticmethod
    def of_excel(url: str, config: dict) -> Authors:
        use_cols= config.get('use_cols',None)
        skip_rows= config.get('skip_rows',None)
        sheetname=config.get('sheet_name',None)
        dataframe = pd.read_excel(url, sheet_name=sheetname, skiprows=skip_rows,usecols=use_cols)
        return Authors(dataframe, config)

    
    @property
    def get_count_col(self):
        return 'number of studies'
    
    @property
    def get_author_name_col(self):
        return self.get_config.get('author_name')
    
    @property
    def count_number_of_studies_per_author(self)->pd.DataFrame:
        preconditions.checkArgument('author_ID' in self.configuration,"Should specify the name of the column for author id")
        preconditions.checkArgument('author_name' in self.configuration,"Should specify the name of the column for author name")
        authorid_col = self.configuration.get('author_ID')
        authorname_col = self.configuration.get('author_name')
        
        d_count = defaultdict(int)
        d_names = defaultdict(SortedSet)
        #create two dictionaries to group by idauthor one with the count another one with
        #the names of the authors
        for _, row in self.dataframe.iterrows():
            authorID = row[authorid_col]
            authorname = row[authorname_col]
            d_count[authorID]+=1
            d_names[authorID].add(authorname)
        #Make a third dict with authors names as keys and counts as values
        d_names_count ={(d_names.get(authorid).pop(0), count) for authorid, count in d_count.items()}       
        #sort the dict by value/count (descending), and then by key/name (ascending)            
        sorted_count = sorted(d_names_count,key=lambda t:(-t[1],t[0]))
        names, counts = zip(*sorted_count)
        return pd.DataFrame(data={authorname_col: names,
                                 'number of studies': counts})

    
    
    @property
    def count_number_of_studies_per_country(self)->pd.DataFrame:
        '''
        @return: A dataframe with the country names and the number 
        '''
        #check the configuration has the columns we need
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkState('country' in self.configuration,"Should specify the name of the column for country")
        #get the column names from the configuration
        id_start = self.configuration.get('id_start')
        country_col = self.configuration.get('country')  
        #create the dataframe with the id of the study and the country
        df_column = self.dataframe[[id_start, country_col]]    
        print(df_column)
        #create a dictionary {country: Set(id_study)}
        dict_countries = dataframes.create_dict_from_multivalued_column(df_column)
               #create a dictionary {id_study: int} that relates a study and the number of different countries that participate in that study
        dict_count = {id:len(ss) for id, ss in dict_countries.items()}
        #sort the dictionary by the number of countries descending
        count_sorted =sorted(dict_count.items(), key=lambda t:t[1], reverse=True)
        names, counts = zip(*count_sorted)
        return pd.DataFrame(data={'countries': names,
                                 'number of studies': counts})

