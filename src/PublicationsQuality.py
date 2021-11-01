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

PublicationsQuality = TypeVar('PublicationsQuality')


@dataclass( order=True)
class PublicationsQuality:
    """

        This class stores all the info about the quality of papers Papers and different Publications written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe  with the publication quality data
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

        """
    quality_df:pd.DataFrame
    configuration: dict


    @property
    def get_config(self):
        '''
            returns the configuration we are working with
        '''
        return self.configuration



    @staticmethod
    def of_csv(url: str, config: dict) -> PublicationsQuality:
        skip_rows= config.get('skip_rows')
        dataframe = pd.read_csv(url, skiprows=skip_rows)
        return PublicationsQuality(dataframe, config, None, None)

    @staticmethod
    def of_excel(url: str, config: dict) -> PublicationsQuality:
        quality_df = pd.read_excel(url, \
                                       sheet_name=config.get("quality_sheet_name"), \
                                       skiprows=config.get('qualtiy_skip_rows'))
        id = config.get('id_start')
        intrinsic_iq = config.get('intrinsic_iq')
        contextual_iq = config.get('contextual_iq')
        quality_df = quality_df[[id, intrinsic_iq, contextual_iq]]
  
        return PublicationsQuality(quality_df, config)
    
    @property
    def get_quality_dataframe(self)->pd.DataFrame:
        return self.quality_df
  
    @property
    def get_id_study_colname(self):
            return self.configuration.get('id_start')
    @property
    def get_contextual_iq_colname(self):
        return self.configuration.get('contextual_iq')
    @property
    def get_intrinsic_iq_colname(self):
        return self.configuration.get('intrinsic_iq')
        
    
    @property
    def count_pairs_per_quality_measure(self)->pd.DataFrame:
        '''
        It return a dataframe with the count of studies per pairs of values of intrinsic and contextual Iq
                 Intrinsic IQ Contextual IQ  number of studies
            0         HIGH          HIGH                 34
            1         HIGH        MEDIUM                  5
            2          LOW          HIGH                 51
            3          LOW        MEDIUM                 13
            4       MEDIUM          HIGH                 38
            5       MEDIUM        MEDIUM                  4
        '''
        col_names = [self.get_intrinsic_iq_colname, self.get_contextual_iq_colname]    
        return dataframes.create_dataframe_facets_count(self.get_quality_dataframe, \
                                            col_names)
    
