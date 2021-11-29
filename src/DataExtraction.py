# -*- coding: utf-8 -*-
import pandas as pd
import dataframes as df
from dataclasses import dataclass
from typing import TypeVar, Dict, List, Set
from builtins import staticmethod
import preconditions
import logging
from sortedcontainers.sortedset import SortedSet

DataExtraction = TypeVar('DataExtraction')
E = TypeVar('E')

@dataclass( order=True)
class DataExtraction:
    """

        This class stores all the info about Papers and different DataExtraction written in a CSV or a xlsx.

        About the atributes, we have 2:
            1. Dataframe: stores the Dataframe of the csv
            2. Configuration: stores a Dict which pair key-value are the different values of configuration

        Besides the attributes, we have generated GETTER and SETTERS for each attributes in the class

        """
    dataframe: pd.DataFrame
    configuration: dict
    columns: Dict[str, List[str]]
    attributes : Dict[str, List[str]]
    

    @property
    def get_df(self)->pd.DataFrame:
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
    def of_csv(url: str, config: dict) -> DataExtraction:
        skip_rows= config.get('skip_rows')
        use_cols= config.get('use_cols')
        dataframe = pd.read_csv(url, skiprows=skip_rows,usecols=use_cols)
        attributes = df.get_attributes(dataframe)
        #list_keys = [k for k in attributes.keys()]
        columns = df.get_columns(dataframe)
        dataframe = df.simplify_start_dataframe(dataframe, columns, attributes)
        return DataExtraction(dataframe, config, columns, attributes)

    @staticmethod
    def of_excel(url: str, config: dict) -> DataExtraction:
        use_cols= config.get('use_cols')
        skip_rows= config.get('skip_rows')
        sheetname=config.get('sheet_name')
        dataframe = pd.read_excel(url, sheet_name=sheetname, skiprows=skip_rows,usecols=use_cols)
        logging.info('Loaded dataframe from {} with {} rows'.format(url, len(dataframe.index)) )
        attributes = df.get_attributes(dataframe)
        #list_keys = [k for k in attributes.keys()]
        columns = df.get_columns(dataframe)
        dataframe = df.simplify_start_dataframe(dataframe, columns, attributes)
        return DataExtraction(dataframe, config, columns, attributes)

    @property
    def get_columns(self)->List[str]:
        return [k for k in self.columns.keys()]
    
    def get_property_values(self, property_name:str):
        return self.attributes.get(property_name)
    
    def get_multivalued_column(self, column_name:str)->pd.DataFrame:
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument(column_name in self.columns.keys(), "Should contain the attribute")  
        id_start = self.configuration.get('id_start')
        df_column = self.dataframe[[id_start, column_name]]     
        return df.create_dataframe_from_multivalued_column(df_column, [id_start,column_name])
    
    def get_single_column(self, column_name:str)->pd.DataFrame:
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument(column_name in self.columns.keys(), "Should contain the attribute")  
        id_start = self.configuration.get('id_start')
        df_column = self.dataframe[[id_start, column_name]]     
        return df_column
  
    def get_single_column_values(self, column_name:str)->Set[E]:
        preconditions.checkArgument(column_name in self.configuration, f"Should specify the name of the column for {column_name}")  
        column_name = self.configuration.get(column_name)
        df_column = self.dataframe[column_name]     
        return SortedSet(df_column.to_list())
    
    def get_single_column_with_multiple_values(self, column_name:str)->pd.DataFrame:
        '''
        A single column with multiple values represents a column that holds a series of comma separated items, for example
        id |  column_name
        ----------------------
        0   | SPUss, Petri Nets
        4   | undetermined
        112 | BPMN    
        113 | BPMN, EPC (Event Driven Process Chain)
        @param column_name:  Name of the column we waht to manage
        @param delimiter: Delimiter used to separate the multiple values included in each item column. The default delimiter is ";"
        @return: It returns a dataframe with the id and the column with single values. For example, the returned dataframe for the previous example is
        id |  column_name
        ----------------------
        0   | SPUss
        0   | Petri Nets
        4   | undetermined
        112 | BPMN    
        113 | BPMN
        113 | EPC (Event Driven Process Chain)   
        '''
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument(column_name in self.columns.keys(), "Should contain the attribute")  
        id_start = self.configuration.get('id_start')
        df_column = self.dataframe[[id_start, column_name]]   
        return df.create_dataframe_from_multivalued_column(df_column, [id_start,column_name], replace_commas=True, transf_function=lambda cad:cad.strip())

    def count_multivalued_column(self, column_name:str)->pd.Series:  
        df =self.get_multivalued_column(column_name)
        return df[column_name].value_counts()\
                              .rename('number of studies',inplace=True)\
                              .rename_axis(column_name)
                              
                
    
    def count_single_column(self, column_name:str)->pd.Series:  
        df =self.get_single_column(column_name)
        return df[column_name].value_counts()\
                              .rename('number of studies',inplace=True)\
                              .rename_axis(column_name)
    
    def count_single_column_with_multiple_values(self, column_name:str)->pd.Series:
        df =self.get_single_column_with_multiple_values(column_name)
        return df[column_name].value_counts()\
                              .rename('number of studies',inplace=True)\
                              .rename_axis(column_name)
    
    def get_faceted_multivalued_column(self, facet1_name:str, facet2_name:str)->pd.DataFrame:
        '''
        @param facet1_name: name of the column that represents the first facet
        @param facet2_name: name of the column that represents the second facet
        @return a dataframe with three columns corresponding to the id of the study, the facet1 and the facet2
        @precondition: The configuration must specify the name of the column for the id of the study
        @precondition: The attribute corresponding to the facet_1 must be included in the colummns to handle
        @precondition: The attribute corresponding to the facet_2 must be included in the colummns to handle
        '''
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument(facet1_name in self.columns.keys(), "Should contain the attribute "+ facet1_name)
        preconditions.checkArgument(facet2_name in self.columns.keys(), "Should contain the attribute "+ facet2_name)  
        id_start = self.configuration.get('id_start')
        df_column = self.dataframe[[id_start, facet1_name, facet2_name]]     
        return df.create_dataframe_from_faceted_multivalued_column(df_column, [id_start,facet1_name, facet2_name])
    
    def get_faceted_multivalued_column_filtered(self, facet1_name:str, facet2_name:str, include:Set[str])->pd.DataFrame:
        '''
        @param facet1_name: name of the column that represents the first facet
        @param facet2_name: name of the column that represents the second facet
        @param include: List of values of the first facet/attribute to be included in the resulting dataset. 
        @return a dataframe with three columns corresponding to the id of the study, the facet1 and the facet2
        @precondition: The configuration must specify the name of the column for the id of the study
        @precondition: The attribute corresponding to the facet_1 must be included in the colummns to handle
        @precondition: The attribute corresponding to the facet_2 must be included in the colummns to handle
        '''
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument(facet1_name in self.columns.keys(), "Should contain the attribute "+ facet1_name)
        preconditions.checkArgument(facet2_name in self.columns.keys(), "Should contain the attribute "+ facet2_name)  
        id_start = self.configuration.get('id_start')
        df_column = self.dataframe[[id_start, facet1_name, facet2_name]]     
        return df.create_dataframe_from_faceted_multivalued_column_filtered(df_column, [id_start,facet1_name, facet2_name], include=include)
    
    def get_faceted_multivalued_single_column_filtered(self, facet1_multivalued_name:str, facet2_single_name:str, include:Set[str])->pd.DataFrame:
        '''
        @param facet1_multivalued_name: name of the column that represents the first facet
        @param facet2_single_name: name of the column that represents the second facet
        @param include: List of values of the first facet/attribute to be included in the resulting dataset. 
        @return a dataframe with three columns corresponding to the id of the study, the facet1 and the facet2
        @precondition: The configuration must specify the name of the column for the id of the study
        @precondition: The attribute corresponding to the facet_1 must be included in the colummns to handle
        @precondition: The attribute corresponding to the facet_2 must be included in the colummns to handle
        '''
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument(facet1_multivalued_name in self.columns.keys(), f"Should contain the attribute {facet1_multivalued_name}")
        preconditions.checkArgument(facet2_single_name in self.configuration, f"Should specify the name of the column for { facet2_single_name}")  
        id_start = self.configuration.get('id_start')
        facet2_single_name = self.configuration.get(facet2_single_name)
        df_column = self.dataframe[[id_start, facet1_multivalued_name, facet2_single_name]]     
        return df.create_dataframe_from_faceted_multivalued_single_column_filtered(df_column, id_start,facet1_multivalued_name, facet2_single_name, include=include)
    
    def create_dataframe_from_faceted_multivalued_column_filled_with_default(self, facet1_name:str, facet2_name:str, include:Set[str], default_facet2_value:str='n/a')->pd.DataFrame:
        '''
        @param facet1_name: name of the column that represents the first facet
        @param facet2_name: name of the column that represents the second facet
        @param include: List of values of the first facet/attribute to be included in the resulting dataset. 
        @param default_facet2_value: 
        @return a dataframe with three columns corresponding to the id of the study, the facet1 and the facet2
        @precondition: The configuration must specify the name of the column for the id of the study
        @precondition: The attribute corresponding to the facet_1 must be included in the colummns to handle
        @precondition: The attribute corresponding to the facet_2 must be included in the colummns to handle
        '''
        preconditions.checkState('id_start' in self.configuration,"Should specify the name of the column for id_start")
        preconditions.checkArgument(facet1_name in self.columns.keys(), "Should contain the attribute "+ facet1_name)
        preconditions.checkArgument(facet2_name in self.columns.keys(), "Should contain the attribute "+ facet2_name)  
        id_start = self.configuration.get('id_start')
        df_column = self.dataframe[[id_start, facet1_name, facet2_name]]     
        return df.create_dataframe_from_faceted_multivalued_column_filled_with_default(df_column, [id_start,facet1_name, facet2_name], include=include, default_facet2_value=default_facet2_value)
    
    def count_faceted_multivalued_column_filtered(self, facet1_name:str, facet2_name:str, include:Set[str])->pd.DataFrame:
        df_faceted = self.get_faceted_multivalued_column_filtered(facet1_name, facet2_name, include)
        return df_faceted[facet2_name].value_counts()\
                              .rename('number of studies',inplace=True)\
                              .rename_axis(facet2_name)
                              
    def count_faceted_multivalued_single_column_filtered(self, facet1_multuvalued_name:str, facet2_single_name:str, include:Set[str])->pd.DataFrame:
        
        df_faceted = self.get_faceted_multivalued_single_column_filtered(facet1_multuvalued_name, facet2_single_name, include)
        print("middle-->", df_faceted)
        facet2_single_name = self.configuration.get(facet2_single_name)
        return df.create_dataframe_facets_count(df_faceted, [facet1_multuvalued_name,facet2_single_name])   
                              
    def count_faceted_multivalued_column(self, facet1_name:str, facet2_name:str)->pd.DataFrame:  
        facet_df =self.get_faceted_multivalued_column(facet1_name, facet2_name)
        return df.create_dataframe_facets_count(facet_df, [facet1_name, facet2_name])
    
    def count_faceted_multivalued_column_filled_with_default(self,facet1_name:str, facet2_name:str, include:Set[str],default_facet2_value:str='n/a' )->pd.DataFrame:
        facet_df =self.create_dataframe_from_faceted_multivalued_column_filled_with_default(facet1_name, facet2_name, include, default_facet2_value)
        return df.create_dataframe_facets_count(facet_df, [facet1_name, facet2_name])
    
    def create_grouping_dict_from_multivalued_colum(self, column_name:str)->Dict[str, Set[str]]:
        '''
        @param column_name: Name of the multivalued column
        @return: A dictionary in which the keys are the different values of the multivalued column and the values
        are sets with the ids of the studies that have that value.
        '''
        dataframe = self.get_multivalued_column(column_name)
        return df.create_dict_from_multivalued_column(dataframe)