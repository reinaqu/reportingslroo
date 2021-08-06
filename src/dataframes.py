# -*- coding: utf-8 -*-
'''
Created on 28 jun. 2020

@author: reinaqu_2
This module contains functions to create dataframes that are
related to slrs or mapping studies in general
'''

from csvbib_utils import *
from typing import TypeVar,Callable,Dict,List, Set
from collections import defaultdict
import pandas as pd 
from sortedcontainers.sortedset import SortedSet
import preconditions
import itertools

E = TypeVar('E')
K = TypeVar('K')
V = TypeVar('V')

def create_dataframe_studies_by_literature_type(studies):
    '''
    INPUT:
        - studies: Dict{id_paper:DictReaderEntry(reference)}
    OUTPUT:
        - dataframe: panda.Dataframe with the following structure:
           * index: type of literature (white or grey)
           * number of studies: number of studies per literature type
    '''

    dict_lit_types= count_studies_by_literature_type(studies)
    
    types, studies_count = zip(*dict_lit_types.items())
    d ={'number of studies': studies_count}
    return pd.DataFrame(data=d, index=types)

def create_dataframe_studies_by_type(studies,filter=None):
    '''
    INPUT:
        - studies: Dict{id_paper:DictReaderEntry(reference)}
    OUTPUT:
        - dataframe: panda.Dataframe with the following structure:
           * index: type of literature (white or grey)
           * number of studies: number of studies per literature type
    '''
    dict=count_studies_by_publication_type(studies,filter)
    sorted_items =sorted(dict.items(),key=lambda it:it[1], reverse=True)
        
    types, studies_count = zip(*sorted_items)
    d ={'number of studies': studies_count}
    return pd.DataFrame(data=d, index=types)

def create_dataframe_studies_by_type2(df:pd.DataFrame, filter:Callable[[E],bool]=None)->pd.DataFrame:
        '''
        INPUT:
            - df: pd.Dataframe
        OUTPUT:
            - dataframe: panda.Dataframe with the following structure:
              * index: type of literature (white or grey)
              * number of studies: number of studies per literature type
        '''
        return df['type'].value_counts()

def create_dataframe_studies_by_year(studies):
    '''
    INPUT:
        - studies: Dict{id_paper:DictReaderEntry(reference)}
    OUTPUT:
        - dataframe: panda.Dataframe with the following structure:
           * year: year of publication of the study
           * white literature: number of studies of white literature per year
           * grey literature: number of studies of grey literature per year
           * total: total number of studies per year
    '''
    dict_wl = count_studies_by_year(studies, lambda s:is_white_literature(s))
    dict_gl = count_studies_by_year(studies, lambda s:is_grey_literature(s))

    years = sorted(dict_wl.keys() | dict_gl.keys())
    wl_count=[]
    gl_count=[]
    l_count =[]
    for year in years:
        wl_count.append(dict_wl.get(year,0))
        gl_count.append(dict_gl.get(year,0))
        l_count.append(dict_wl.get(year,0)+dict_gl.get(year,0))
        
    d ={'year': years,
        'white literature': wl_count,
        'grey literature':gl_count,
        'total': l_count}
    return pd.DataFrame(data=d)

def create_dataframe_studies_by_country(studies):
    dict = count_studies_by_country(studies, lambda s:not is_country_null(s))

    countries, studies_count = zip(*dict.items())
    d ={'countries': countries,
        'number of studies': studies_count}
    return pd.DataFrame(data=d)



def create_dataframe_from_excel(excel_datafile, sheet_name, index_col):
    df= pd.read_excel(excel_datafile,
            sheet_name=sheet_name,
            header=0,
            na_values="-",
            index_col=False,
            keep_default_na=True
            )
    
    return df.set_index(index_col)
  
def create_dataframe_studies_contextualIQ(studies, filter=None):
    dict_qualities = calculate_studies_contextualIQ(studies, filter)
    studies_ids = dict_qualities.keys()
    completeness,contextualIQ= zip(*dict_qualities.values())
           
    d ={'ContextualIQ': contextualIQ,
        }
    res= pd.DataFrame(data=d, index=studies_ids)
    res.index.name=ID_PAPER
    return res

def create_dataframe_quality_facets(contextual_df,quality_df): 
    
    data = quality_df['IntrinsicIQ'].tolist()
    contextual_df.insert(0,'IntrinsicIQ', data,True)
    return contextual_df
    
                        
def create_dataframe_intrinsicIQ_count(quality_df):
    #df= quality_df[[ID_PAPER,'IntrinsicIQ']].groupby(['IntrinsicIQ']).agg(name=('number of studies','count'))
    df=quality_df.groupby(['IntrinsicIQ']).size().reset_index(name='number of studies')
    return df

def create_dataframe_contextualIQ_count(contextualIQ_df):
    #df= quality_df[[ID_PAPER,'IntrinsicIQ']].groupby(['IntrinsicIQ']).agg(name=('number of studies','count'))
    df=contextualIQ_df.groupby(['ContextualIQ']).size().reset_index(name='number of studies')
    return df

def create_dataframe_facets_count(facet_df:pd.DataFrame, facet_names:List[str])->pd.DataFrame:
    #df= quality_df[[Idf=df.set_index(FOCUS)D_PAPER,'IntrinsicIQ']].groupby(['IntrinsicIQ']).agg(name=('number of studies','count'))
    df=facet_df.groupby(facet_names).size().reset_index(name='number of studies')    
    return df

def fill_gaps_with_zeros(df:pd.DataFrame)-> None:
    '''
        Input: A dataframe with an integer index and an integer column
        It modifies the dataframe and adds zero values.
        For example if the dataframe represents the mumber of studies by year
        and thera are some years with no studies, we add those years
        with a zero value
    '''
    index_values= df.index.values
    min_value = min(index_values)
    max_value = max(index_values)
    for indx in range(min_value, max_value+1):
        if not indx in df.index:
            df[indx]= 0
            
def simplify_start_dataframe (df: pd.DataFrame,columns:Dict[str, List[str]], attributes:Dict[str, List[str]])->pd.DataFrame:
    '''
    @param df: dataframe with Y/N columns to mix in just one column
    @param column: Dict[str, List[str]] Dic
    @param attributes: Dict[str, List[str]]
    @return a new dataframe 
    '''
    
    res= pd.DataFrame()
#     print('columns')
#     for key, value in columns.items():
#         print(key, '-->', value)
#     print('attributes', attributes)
    # Example of column : ['Logistics activities : organization', 'Logistics activities : planning]']
    for col, list_values in columns.items():
        if (len(list_values)>0):
            df_col = df[list_values]
            df_col = merge_columns_dataframe (df_col, col, attributes[col])
        else:
            df_col = df[[col]]
            #print("simple column", col, df_col)
        res = pd.concat([res, df_col], axis=1)
 
    return res
   
def merge_columns_dataframe (df:pd.DataFrame, col: str, attributes: List[str])->pd.DataFrame: 
    '''
    @param df: dataframe with Y/N columns to mix in just one column
    @param col: name of the resulting column in the new dataframe
    @param attributes: list with the values in the resulting column
    @return: a new dataframe with just one column
        Example:
        df is the dataframe 
                    Logistics activities : organization Logistics activities : planning]
        0                                      N                                N
        1                                      Y                                N
        2                                      N                                Y
        3                                      Y                                Y
        col is "Logistics activities"
        attributes is ['organization', 'planning]']
        The result is the dataframe
                    Logistics activities 
        0            ''
        1            'organization'
        2            'planning]'   
        3            'organization; planning]'
        
    '''
    res =[]
    for tuple in df.itertuples(index=False):
        values =""
        for indx, value in enumerate(tuple):           
            if str(value) == 'Y':
                #print (indx, value)
                values+= ";" +attributes[indx]
        #the first character is always a semicolon, I remove it
        res.append(values[1:])    
    return pd.DataFrame(data=res, columns=[col])

def get_attributes(df:pd.DataFrame)-> Dict[str, List[str]]:
    '''
    @param df: dataframe with Id paper, tile, data extraction columns of strings and Y/N values
    @return a dictionary that groups columns by data extraction field (attributes) and has as values the list 
            of the possible attributes (if they are Y/N columns) or an empty list if it is a str attribute
    Example:
    df is the dataframe
        ID Paper    Title     Logistics activities : organization Logistics activities : planning]     Modelling language
    0   ...                                                                    
    1   ...
    The result is the dictionary
     {'ID Paper': [], 
      'Title': [], 
      'Logistics activities': ['organization', 'planning]'], 
      'Modelling language':[]}                                 
    '''
    res = defaultdict(list)
    for column_name in df: 
        splits = column_name.split(sep=":")
        attr_name=splits[0].strip()
        if len(splits) > 1:
            #Start has a bug and generates the name of the last columnn of an attribute
            #with a ]
            value= splits[1].replace("]","").strip()
            res[attr_name].append(value)
        else:
            res[attr_name]=[]
        
    return res

def get_columns(df:pd.DataFrame)-> Dict[str, List[str]]:
    '''
    @param df: dataframe with Id paper, tile, data extraction columns of strings and Y/N values
    @return a dictionary that groups columns by data extraction field (attributes) and has as values the list 
            of the columns (if they are Y/N columns) or an empty list if they are str attributes 
    Example:
    df is the dataframe
        ID Paper    Title     Logistics activities : organization Logistics activities : planning]     Modelling language
    0   ...                                                                    
    1   ...
    The result is the dictionary
     {'ID Paper': [], 
      'Title': [], 
      'Logistics activities': ['Logistics activities : organization', 'Logistics activities : planning]'], 
      'Modelling language':[]}                                 
    '''
    res = defaultdict(list)
    for column_name in df: 
        splits = column_name.split(sep=":")
        attr_name=splits[0].strip()
        if len(splits) > 1:
            value= column_name     
            res[attr_name].append(value)
        else:
            res[attr_name]=[]         
    return res

def create_dataframe_from_multivalued_column (df:pd.DataFrame, column_names:List[str], replace_commas:bool=False, transf_function:Callable=None)->pd.DataFrame:
    preconditions.checkArgument(len(column_names)==2, 'The list only must have two column names: the id column_name and the column name that is the aim of the dataframe')
    list_id=[]
    list_values=[]
    for id, values in df.itertuples(index=False):
        if values!=None:
            if replace_commas==True:
                values = values.replace(",",";")             
            for value in values.split(";"):
                list_id.append(id)
                if transf_function != None:
                    value = transf_function(value)
                list_values.append(value)
        ##TODO -             
    return pd.DataFrame({column_names[0]:list_id, column_names[1]:list_values})   

def create_dataframe_from_faceted_multivalued_column (df:pd.DataFrame, column_names:List[str])->pd.DataFrame:
    preconditions.checkArgument(len(column_names)==3, 'The list only must have three column names: the id column_name, the facet 1 column name and the facet 2 column name')
    list_id=[]
    list_values_facet1=[]
    list_values_facet2=[]
    for id, facet1, facet2 in df.itertuples(index=False):
        l_id=[id]
        l_facet1=[None]
        if facet1!=None:
            l_facet1=facet1.split(";")
        l_facet2=[None]
        if facet2!=None:
            l_facet2= facet2.split(";")
        for id, f1, f2 in itertools.product(l_id,l_facet1, l_facet2):
            list_id.append(id)
            list_values_facet1.append(f1)
            list_values_facet2.append(f2)               
        ##TODO -             
    return pd.DataFrame({column_names[0]:list_id, column_names[1]:list_values_facet1, column_names[2]:list_values_facet2})   
       
def create_dict_from_multivalued_column (df:pd.DataFrame)->Dict[str, Set[str]]:
    '''
    @return A dictionary whose keys are the different values, and the values are
    a sortedset with the different ids
    '''
    res = defaultdict(SortedSet)
    for id, values in df.itertuples(index=False):
        if values!=None:
            for value in values.split(";"):
               res[value].add(id)        ##TODO -             
    return res   

def create_dict_from_single_column (df:pd.DataFrame)->Dict[str, Set[str]]:
    '''
    @return A dictionary whose keys are the different values, and the values are
    a sortedset with the different ids
    '''
    res = defaultdict(SortedSet)
    for id, value in df.itertuples(index=False):
            res[value].add(id)        ##TODO -             
    return res   

def translate_index_dataframe (df:pd.DataFrame ,translation:Dict[K,V] )->pd.DataFrame:
    list_indx=[]
    list_values=[]
    for indx, value in df.items():
        list_indx.append(translation.get(indx, None))
        list_values.append(value)
    return pd.DataFrame({'number of studies':list_values},
                        index=list_indx)    
    

def exclude_index_values_from_series( serie: pd.Series, exclusion:List[E])->pd.Series:
    res = serie
    if (len(exclusion)>0):
        index_values = serie.index.values.tolist()
        index_values = [value for value in index_values if value not in exclusion]
        res = serie.filter(index_values)
    return res 