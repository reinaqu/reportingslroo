# -*- coding: utf-8 -*-
'''
Created on 29 jun. 2020

@author: reinaqu_2
This module contains functions to create dataframes that are
related to the smart contract domain
'''
import pandas as pd
from sc_utils import *

def create_dataframe_languages_by_blokchain_platform(languages):
    '''
    INPUT:
        - languages: Dict(language: [Dict{id_paper:DictReaderEntry(reference)}])
    OUTPUT:
        - dataframe: panda.Dataframe with the following structure:
           * index: blockain platform
           * number of languages: number of languages per blockchain platform
    '''

    dict_lang_bc= count_languages_by_blockchain(languages, lambda l:not is_blockchain_null(l) and not is_blockchain_na(l))

    ordered =sorted(dict_lang_bc.items(),key=lambda it:it[1], reverse=True)
    bc_platforms, languages_count = zip(*ordered)
    d ={'number of languages': languages_count}
    return pd.DataFrame(data=d, index=bc_platforms)


def create_dataframe_languages_by_context_and_kind(languages):
    
    dict_pairs = count_languages_by_context_and_kind(languages)
    
    bc_academia,languages_kind,languages_count = unzip_pairs_dict(dict_pairs)
          
    d ={'kind of language':languages_kind,
        'number of languages': languages_count}
    return pd.DataFrame(data=d, index=bc_academia)


def create_dataframe_languages_by_paradigm_and_kind(languages):
    
    dict_pairs = count_languages_by_paradigm_and_kind_flattened(languages)
       
    paradigm,languages_kind,languages_count = unzip_pairs_dict(dict_pairs)
          
    d ={'kind of language':languages_kind,
        'number of languages': languages_count}
    return pd.DataFrame(data=d, index=paradigm)

# def create_labels_names_languages_by_paradigm(languages, filter=None):
#     
#     dict_pairs = group_languages_by_paradigm_and_kind(languages, filter)
#     
#     dict_mappings={'Imperative':'0001', 'Declarative':'0010', 'Symbolic':'0100','Unknown':'1000','Declarative,Imperative':'0011'}
# 
#     labels = {dict_mappings[key[0]]:get_languages_ids(list_studies) for key, list_studies in dict_pairs.items()}
#     
#     names=['Imperative', 'Declarative','Symbolic','Unknown']
#     return labels, names

def create_labels_names_languages_by_paradigm(languages, filter=None):
    
    dict_pairs = count_languages_by_paradigm_and_kind(languages, filter)
    
    dict_mappings=OrderedDict({'Imperative':'001', 'Declarative':'010', 'Symbolic':'100','Declarative,Imperative':'011'})
    labels = OrderedDict({dict_mappings[key[0]]:count for key, count in dict_pairs.items()})
    return labels


def create_dataframe_languages_by_context_and_type(languages):
    dict_pairs = count_languages_by_context_and_type(languages)
    
    bc_academia,languages_type,languages_count = unzip_pairs_dict(dict_pairs)
          
    d ={'type of language':languages_type,
        'number of languages': languages_count}
    return pd.DataFrame(data=d, index=bc_academia)

def create_dataframe_languages_by_kind_and_type(languages):
    dict_pairs = count_languages_by_kind_and_type(languages)
    
    languages_kind,languages_type,languages_count = unzip_pairs_dict(dict_pairs)
          
    d ={'type of language':languages_type,
        'number of languages': languages_count}
    return pd.DataFrame(data=d, index=languages_kind)


def create_dataframe_use_cases_count(languages, df_usecases):
    '''
    INPUT: 
        -studies : list o studies [OrderedDict(('Paper ID':id), ('Zone', Country_name)]
        -df_usecases: dataframe with the following requirements:
            * It should have as index the ID_PAPER
            * It should have a column (named Clasificación) with the use cases
            * The use cases of the study should have the format uc1/uc2/...
              For example, Financial/Game/Notary/Others

    OUTPUT: 
        - a dataframe
    ''' 
    dicc = count_use_cases (languages, df_usecases)
    list_abbr =[(get_usecase_abbrv(key), value) for key,value in dicc.items()]
    ordered =sorted(list_abbr,key=lambda it:it[1], reverse=True)
    use_cases, count = zip(*ordered)
   
    d ={'number of use cases': count}
    res= pd.DataFrame(data=d, index=use_cases)
    #res.index.name='Use cases'
    return res

def create_dataframe_count_languages_by_focus(df_lan):
    # iterate through each row and select  
    # 'Name' and 'Age' column respectively. 
    lst=[]
    for index, row in df_lan.iterrows(): 
        conj_focuses = get_focus(row[FOCUS])
        lst = lst + list(conj_focuses)
    dicc = Counter(lst)
  
    ordered = sorted((get_focus_abbrv(key), value) for key, value in dicc.items() if value >1)
    focuses, count = zip(*ordered)
    d ={'number of languages': count}
    df= pd.DataFrame(data=count, index=focuses)        
    df.index.name='Focus'
    
    #df=df_lan.groupby([FOCUS]).size().reset_index(name='number of languages')
        
    #df=df.set_index(FOCUS)
    return df

def create_dicc_group_languages_by_focus(df_lan):
    # iterate through each row and select  
    # 'focuses' and 'languages' column respectively. 

    dicc =defaultdict(list)
    for index, row in df_lan.iterrows(): 
        conj_focuses = get_focus(row[FOCUS])
        for focus in conj_focuses:
            dicc[focus].append(index)

    ordered = sorted((key, sorted(value)) for key, value in dicc.items())
   
    #df=df_lan.groupby([FOCUS]).size().reset_index(name='number of languages')
        
    #df=df.set_index(FOCUS)
    return ordered


def create_dataframe_implementation_language_ordered_by(df_lang_feat, order_criteria):
    filter = df_lang_feat['Kind'] == 'Implementation'
    df_lang_feat['Paradigm'] = df_lang_feat['Paradigm'].str.strip()
    df_lang_feat['Level'] = df_lang_feat['Level'].str.strip()
    df_lang_feat['Focus'] = df_lang_feat['Focus'].str.strip()
    res = df_lang_feat[filter].sort_values(by=order_criteria)
    return res

def create_dataframe_specification_language_ordered_by(df_lang_feat, order_criteria):
    filter = df_lang_feat['Kind'] == 'Specification'
    df_lang_feat['Paradigm'] = df_lang_feat['Paradigm'].str.strip()
    df_lang_feat['Level'] = df_lang_feat['Level'].str.strip()
    df_lang_feat['Focus'] = df_lang_feat['Focus'].str.strip()
    res = df_lang_feat[filter].sort_values(by=order_criteria)
    return res
