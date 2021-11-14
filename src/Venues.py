# -*- coding: utf-8 -*-
import pandas as pd
import dataframes
from dataclasses import dataclass
from typing import TypeVar
import preconditions

Venues = TypeVar('Venues')



@dataclass(frozen=True, order=True)
class Venues:
    """

        This class stores all the info about Papers and different Publications written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

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
    def of_dataframe(dataframe:pd.DataFrame, config: dict)->Venues:
        return Venues (dataframe, config)
    @staticmethod
    def of_csv(url: str, config: dict) -> Venues:
        skip_rows= config.get('skip_rows')
        dataframe = pd.read_csv(url, skiprows=skip_rows)
        return Venues(dataframe, config)

    @staticmethod
    def of_excel(url: str, config: dict) -> Venues:
        use_cols= config.get('use_cols')
        skip_rows= config.get('skip_rows')
        sheetname=config.get('sheet_name')
        dataframe = pd.read_excel(url, sheet_name=sheetname, skiprows=skip_rows,usecols=use_cols)
        return Venues(dataframe, config)

    @property
    def count_number_of_studies_per_venue(self)->pd.DataFrame:
        '''
        @return: it returns a dataframe with the venues and the number of studies published 
        in that venue. The dataframe is ordered descending by the number of studies
        @rtype:pd.DataFrame
        '''
        preconditions.checkState('venue' in self.configuration,"Should specify the name of the column for venue")
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkState('type' in self.configuration,"Should specify the name of the column for paper id")
        venue_col = self.configuration.get('venue')
        paperid_col = self.configuration.get('id_start')
        type_col = self.configuration.get('type')
        return dataframes.create_dataframe_facets_count(self.dataframe, [venue_col,type_col])\
                         .sort_values(['number of studies', type_col, venue_col], ascending=[False, False,True])\
                         .reset_index(drop=True)
                         
                        
#         return self.dataframe.groupby([venue_col, type_col])\
#                              .count()\
#                              .sort_values([paperid_col,type_col],ascending=False)

    @property
    def count_venues_per_type(self)->pd.DataFrame:
        df_count = self.count_number_of_studies_per_venue
        type_col = self.configuration.get('type')
        return dataframes.create_dataframe_facets_count(df_count, [type_col])

    def get_venue(self, id_study:str)->str:
        '''
        @param id_study: the id of the study we are looking for
        @return the venue associated to the id, or None id the id_study is not found
        '''
        preconditions.checkState('venue' in self.configuration,"Should specify the name of the column for venue")
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        venue_col = self.configuration.get('venue')
        paperid_col = self.configuration.get('id_start')
        df = self.dataframe
        values= df.loc[df[paperid_col] == id_study][venue_col].values
        res=None
        if (len(values)>0):
            res = values[0]
        return res
       
        