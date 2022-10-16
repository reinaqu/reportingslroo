# -*- coding: utf-8 -*-
'''
Created on 6 ago. 2021

@author: reinaqu_2
'''
import commons

searches_conf = {'ACM': [0, 6, 7, 185],
                       'Springer': [1, 8, 9, 193,194,195],
                       'Science Direct': [2, 12, 13,187,188],
                       'IEEE': [3,10,11,186],
                       'Scopus':[4,14,15,189],
                       'Google Academic': [5,16,17,190,191,192],
                       'Backward Snowballing':[n for n in range(18,185)]+[n for n in range(315,330)]+[342,343,344,346,348,350,352,353,354],
                       'Forward Snowballing':[n for n in range(196,315)]+[n for n in range(320,342)]+[345,347,349,351,355,356]}

config_publ ={'skip_rows': 7, 
             'sheet_name':'Papers',
             'use_cols':[0,1,2,3,4,9,10,11,12,13,14,15,16,17,18,19],
             'type': 'Type',
             'doi':'DOI',
             'year':'Year',
             'id_start': 'ID Paper',
             'title': 'Title',
             'id_search': 'ID Search Session',
             'searches_datasources': commons.invert_dict(searches_conf),
             'authors':'Authors',
             'publication-type':'Type',
             'venue':'Journal',
             'keywords':'Keywords',
             'abstract': 'Abstract',
             'quality_sheet_name':'Quality',
             'quality_skip_rows':0,
             'contextual_iq': 'Contextual IQ',
             'intrinsic_iq': 'Intrinsic IQ',
             'completness': 'Completness'
}
    
config_auth ={'author_ID':'Author ID',
                  'author_name':'Author name',
                  'id_start':'Paper ID',
                  'sheet_name':'authors',
                  'country':'Country',
                  'skip_rows':0}

config_venues ={'venue':'Venue',
                    'id_start':'Paper ID',
                    'type':'Type',
                    'sheet_name':'venues',
                    'skip_rows':0}

    
    
config_data_extraction ={'skip_rows': 7, 
             'sheet_name':'Papers',
             'use_cols':[0,1,9]+[n for n in range(34,135)],
             'id_start': 'ID Paper',
             'title': 'Title',
             'year':'Year'
             }
