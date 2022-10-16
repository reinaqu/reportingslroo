# -*- coding: utf-8 -*-
'''
Created on 29 jun. 2020

@author: reinaqu_2
'''
from commons import *
import numpy as np
import pandas as pd



    
def is_blockchain_null(blockchain):
    return blockchain == 'null'

def is_blockchain_na(blockchain):
    return blockchain == 'n/a' 



def completeness(study):
    qa1 = has_contribution_type(study)
    qa2 = has_paradigm(study)
    qa3 = has_blockchain(study)
    qa4 = has_dsl_type(study)
    qa5 = has_focus(study)
    qa6 = has_institution(study)
    qa7 = has_institution_origin(study)
    qa8 = has_challenges(study)
    qa9= has_use_cases(study)
    qa10 = has_language_kind(study)
    return (qa1+qa2+qa3+qa4+qa5+qa6+qa7+qa8+qa9+qa10)/10

def contextual_IQ(study):
    c = completeness(study)
    if c>0.5:
        res='High'
    elif c>0.2:
        res='Medium'
    else:
        res='Low'
    return (c, res)
    
def has_process_lifecycle(study):
    LANGUAGE_NAME='Name'
    return 0 if study[LANGUAGE_NAME]=='null' else 1

def has_paradigm(study):
    UNDETERMINED_PARADIGM="Paradigm : Undetermined}"
    return 0 if study[UNDETERMINED_PARADIGM]=='Y' else 1

def has_blockchain(study):
    SUPPORTED_BY_BLOCKCHAIN='Supported by blockchain platform : Yes'
    BLOCKCHAIN_NAME="Blockchain name"
    return 0 if study[SUPPORTED_BY_BLOCKCHAIN]=='Y' and study[BLOCKCHAIN_NAME]=='null' else 1

def has_dsl_type(study):
    STANDALONE='DSL Type : Standalone'
    EXTENSION='DSL Type : Extension}'
    return 0 if study[STANDALONE]=='N' and study[EXTENSION]== 'N' else 1

def has_focus(study):
    FOCUS='Focus'
    return 0 if study[FOCUS]=='null' else 1

def has_institution(study):
    INSTITUTION='Institution name'
    return 0 if study[INSTITUTION]=='null' else 1

def has_institution_origin(study):
    INSTITUTION='Institution name'
    ACADEMIA = 'Insitution origin : Academia'
    INDUSTRY = 'Insitution origin : Industry}'
    return 0 if study[INSTITUTION]=='null' and (study[ACADEMIA]=='Y' or study[INDUSTRY]== 'Y') else 1


def has_challenges(study):
    CHALLENGES='Challenges'
    return 0 if study[CHALLENGES]=='null' else 1
 
def has_use_cases(study):
    USE_CASES='Use cases'
    return 0 if study[USE_CASES]=='null' else 1

def has_language_kind(study):
    IMPLEMENTATION='Kind : Implementation'
    SPECIFICATION='Kind : Specification'
    UNKNOWN='Kind : Unknown}'

    return 0 if study[IMPLEMENTATION]=='N' and study[SPECIFICATION]=='N' and study[UNKNOWN]=='N' or study[UNKNOWN]=='Y' else 1

def count_use_cases (languages, df_usecases):
    '''
    INPUT: 
        -studies : list o studies [OrderedDict(('Paper ID':id), ('Zone', Country_name)]
        -df_usecases: dataframe with the following requirements:
            * It should have as index the ID_PAPER
            * It should have a column (named Clasificación) with the use cases
            * The use cases of the study should have the format uc1/uc2/...
              For example, Financial/Game/Notary/Others

    OUTPUT: 
        - {language:set(use cases)} dictionary whose keys are the languages names and whose
          values are sets of the use cases found for that language
    ''' 
    dict= group_use_cases_by_languages(languages, df_usecases)
    lista=[]
    for conj in dict.values():
        lista= lista +list(conj)
    return Counter(lista)
    
    

def group_use_cases_by_languages (languages, df_usecases):
    '''
    INPUT: 
        -studies : list o studies [OrderedDict(('Paper ID':id), ('Zone', Country_name)]
        -df_usecases: dataframe with the following requirements:
            * It should have as index the ID_PAPER
            * It should have a column (named Clasificación) with the use cases
            * The use cases of the study should have the format uc1/uc2/...
              For example, Financial/Game/Notary/Others

    OUTPUT: 
        - {language:set(use cases)} dictionary whose keys are the languages names and whose
          values are sets of the use cases found for that language
    ''' 
    return {language: extract_use_cases(studies,df_usecases) for language, studies in languages.items()}

def extract_use_cases(studies, df_usecases):
    '''
    INPUT: 
        -studies : list o studies [OrderedDict(('Paper ID':id), ('Zone', Country_name)]
        -df_usecases: dataframe with the following requirements:
            * It should have as index the ID_PAPER
            * It should have a column (named Clasificación) with the use cases
            * The use cases of the study should have the format uc1/uc2/...
              For example, Financial/Game/Notary/Others

    OUTPUT: 
        - A set with all the use cases of all the studies in the list
    '''
    conj=set()
    for study in studies:
        conj=conj.union(get_use_cases(study, df_usecases))
    return conj

def get_use_cases(study,df_usecases):
    '''
    INPUT: 
        -study : OrderedDict(('Paper ID':id), ('Zone', Country_name)
        -df_usecases: dataframe with the following requirements:
            * It should have as index the ID_PAPER
            * It should have a column (named Clasificación) with the use cases
            * The use cases of the study should have the format uc1/uc2/...
              For example, Financial/Game/Notary/Others

    OUTPUT: 
        - A set with all the use cases of the study
    '''
    conj=set()
    #Get the id of the study
    id_slr=study[ID_PAPER].strip()
    #Query de dataframe to get all the use cases
    uc=df_usecases.loc[int(id_slr)].loc['Clasificación']
    #As there can be nan data, we only can split if the data is not nan
    if not pd.isna(uc):
        c=set(uc.split("/"))
        c={pal.strip() for pal in c}
        conj=conj.union(c)
    return conj


def get_focus(focus):
    '''
    INPUT: 
        -study : OrderedDict(('Paper ID':id), ('Zone', Country_name)
        -df_usecases: dataframe with the following requirements:
            * It should have as index the ID_PAPER
            * It should have a column (named Clasificación) with the use cases
            * The use cases of the study should have the format uc1/uc2/...
              For example, Financial/Game/Notary/Others

    OUTPUT: 
        - A set with all the use cases of the study
    '''
    conj=set()

    #As there can be nan data, we only can split if the data is not nan
    if not pd.isna(focus):
        c=set(focus.split("/"))
        c={pal.strip() for pal in c}
        conj=conj.union(c)
    return conj

def get_focus_abbrv(focus):
    abrev= {'Business Process':'BP',
            'Contract Composition': 'ConComp',
            'Financial': 'Financial',
            'Formalisation':'Formal',
            'General Purpose':'GP',
            'Improve Development':'ImpDev',
            'Increase Level of Abstraction':'IncLoA',
            'Interactions':'Inter',
            'Legal': 'Legal',
            'Model-driven':'MD',
            'Natural Language':'NL',
            'Ontology':'Ontol',
            'Optimization':'Optim',
            'Oracles':'Oracles',
            'Other':'Other',
            'Privacy':'Privacy',
            'Safety':'Safety',
            'Security':'Secur',
            'Separation of Concerns':'SoC',
            'Service-oriented':'SO',
            'Trust':'Trust',
            'Verification':'Verif',
            'Virtual Machine':'VM',
            'Visual Specification':'VisSpec'}
    return abrev[focus]  

def get_usecase_abbrv(usecase):
    abrev= {'Data Provenance':'DataProv',
            'Distributed Systems Security':'DSS',
            'Financial': 'Financial',
            'Game':'Game',
            'IoT':'IoT',
            'Legal Contracts': 'LegContr',
            'Library':'Library',
            'Notary':'Notary',
            'Others':'Others',
            'Public Sector': 'PubSec',
            'Sharing Economy': 'SharEco',
            'Wallet':'Wallet',
            'null': 'null'}
    return abrev[usecase]

