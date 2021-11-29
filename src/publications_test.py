# -*- coding: utf-8 -*-
'''
Created on 28 jun. 2020

@author: reinaqu_2
'''
from graphics_utils import *
from dataframes import *
from commons import *
from sc_utils import *
from sc_latex import *
import Publications as pub
import Dashboard as dashbd
import DashboardLatex as dashbdlat
import bibutils
import Authors as auth
import Venues as ven
import DataExtraction as datext
import DashboardDataExtraction as datextdash
import configurations
import KeywordClusterer as keyclus
import test_utils

from dataframes_sc import *
import locale
if __name__ == "__main__":
   
    REPORT_FILE="../data/report.v.0.2.52.xls"
    AUTHORS_FILE ="../out/authors.csv"
    AUTHORS_COUNT_FILE ="../out/authors_count.csv"
    COUNTRIES_COUNT_FILE ="../out/countries_count.csv"
    VENUES_COUNT_FILE ="../out/venues_count.csv"
    VENUES_FILE ="../out/venues.csv"
    BIBTEX_FILE ="../out/studies.bib"
    DATA_EXTRACTION_FILE ="../out/data_extraction.v.0.2.42.csv"
    FULL_REPORT_FILE="../data/report-all.v.0.2.37.xls"
    AUTHORS_INPUT_FILE ="../data/all-authors-2.0.xlsx"
    VENUES_INPUT_FILE ="../data/all-venues-2.0.xlsx"
    CONTRIBUTION_TYPE_FILE="../out/contribution_type.csv"
    PROCESS_LIFECYCLE_FILE="../out/process_lifecycle.csv"
    LIFECYCLE_ANALISIS_FILE="../out/lifecycle_analysis.csv"
    DOMAIN_FILE="../out/domain.csv"
    LOGISTIC_COVERAGE_FILE="../out/logistics_coverage.csv"
    CHALLENGE_FILE="../out/challenge.csv"
    FOCUS_FILE="../out/focus.csv"
    MOD_LANG_FILE="../out/modelling_language.csv"
    MOD_LANG_TYPE_FILE="../out/modelling_language_type.csv"
    EVENT_PRODUCER_FILE="../out/event_producer_language.csv"
    EVENT_LANGUAGE_FILE="../out/event_processing_language.csv"
    EVENT_MODEL_FILE="../out/event_model.csv"
    CITATION_FILE ="../data/citations_per_paper.xlsx"
    KEYWORDS_FILE = "../out/keywords.csv"
    MAP_FILE='../data/countries.geojson'


    publ_full = pub.Publications.of_excel(FULL_REPORT_FILE,configurations.config_publ)
#     print(publ_full.count_studies_per_datasource)
#     publ_full.count_studies_per_datasource.to_csv("../out/studies_per_datasource.csv")
#     db_full = dashbd.Dashboard.of(publ_full)
#     db_full.create_piechart_studies_by_datasource
    
    publ = pub.Publications.of_excel(REPORT_FILE,configurations.config_publ)
    print (publ.get_df)
    print(publ.count_studies_by_type)
      
    db = dashbd.Dashboard.of(publ)
   
    data_df = datext.DataExtraction.of_excel(REPORT_FILE,configurations.config_data_extraction)
#     data_df.dataframe.to_csv(DATA_EXTRACTION_FILE)
    datadash = datextdash.DashboardDataExtraction.of(data_df)
    
    test_utils.show_quality_bubble_plot(REPORT_FILE, datadash)



#     db.create_piechart_studies_by_type
    #for doi in pub.get_normalized_dois:
    #    print (doi)
     
#     print(publ.count_studies_by_year)
#     db.create_plot_studies_by_year

    dblat = dashbdlat.DashboardLatex.of(publ)
#     dblat.load_db_from_dblp
#     authors_df = dblat.get_authors_dataframe_from_db
#     authors_df.to_csv(AUTHORS_FILE, index=False)
    
    #Generate authors count dataframe
#     authors = auth.Authors.of_dataframe(authors_df, config_auth)
#     authors = auth.Authors.of_excel(AUTHORS_INPUT_FILE, configurations.config_auth)
#     print (authors)
#     authors_count_df = authors.count_number_of_studies_per_author
#     authors_count_df.to_csv(AUTHORS_COUNT_FILE)
#       
#     countries_count_df = authors.count_number_of_studies_per_country
#     countries_count_df.to_csv (COUNTRIES_COUNT_FILE)
#     db.set_authors(authors)
#     db.set_geojson_file(MAP_FILE)
#     db.create_map_countries
#     
    
    #Generate venues dataframe
#     venues_df =dblat.get_venues_dataframe_from_db
#     venues_df.to_csv(VENUES_FILE, index=False)

    venues= ven.Venues.of_excel(VENUES_INPUT_FILE, configurations.config_venues)
#     #venues = ven.Venues.of_dataframe(venues_df, config_venues)
#     print (venues)
#     venues_count_df = venues.count_number_of_studies_per_venue
#     print(venues_count_df)
#     venues_count_df.to_csv(VENUES_COUNT_FILE)
#     print(venues.count_venues_per_type)
#     #Generate latex
#     dblat.generate_bibtex_from_dblp(BIBTEX_FILE)
#  
#     #Generate cite
#     print(dblat.generate_cite_from_dblp())
    

#     publ.set_citations_dataframe_from_excel(CITATION_FILE, ['GoogleScholar','Scopus'])
#     publ.citation_df.to_csv("../out/citations.csv")
#     dblat.generate_citations(['GoogleScholar','Scopus'])
    

    
#     contrib_type_df=data_df.get_multivalued_column("ContributionType")
#     contrib_type_df.to_csv(CONTRIBUTION_TYPE_FILE)
#     print(data_df.count_multivalued_column("ContributionType"))
#        
#     datadash.create_bar_count_multivalued_column("ContributionType", rotation=45)
#     datadash.create_piechart_count_multivalued_column("ContributionType")

#     lifecicycle_df=data_df.get_multivalued_column("Process lifecycle phase")
#     lifecicycle_df.to_csv(PROCESS_LIFECYCLE_FILE)
#     print(data_df.count_multivalued_column("Process lifecycle phase"))
#        
#        
#     dict_plc_translation={'process monitoring':'monitoring',\
#                        'process identification': 'identification',\
#                        'process analysis' : 'analysis',\
#                        'process redesign':'redesign',\
#                        'process discovery':'discovery',\
#                        'process implementation':'implementation',\
#                        'undetermined':'undetermined'
#                        }      
#     datadash.create_bar_count_multivalued_column("Process lifecycle phase", rotation=45, translation = dict_plc_translation)
#     datadash.create_piechart_count_multivalued_column("Process lifecycle phase")

    #faceted_df = data_df.get_faceted_multivalued_column("Process lifecycle phase", "Process analysis type")
#     faceted_df = data_df.get_faceted_multivalued_column_filtered("Process lifecycle phase", "Process analysis type", include={'process analysis'})
#     print(faceted_df)
#     faceted_df.to_csv(LIFECYCLE_ANALISIS_FILE)
#     
#     faceted_full_df = data_df.create_dataframe_from_faceted_multivalued_column_filled_with_default("Process lifecycle phase", "Process analysis type", include={'process analysis'})
#     print(faceted_full_df)
#     
#     print(data_df.count_faceted_multivalued_column_filtered("Process lifecycle phase", "Process analysis type", include={'process analysis'}))
#     datadash.create_bar_count_faceted_multivalued_column_filtered("Process lifecycle phase", "Process analysis type", include={'process analysis'}, rotation=45, exclude=['undetermined'])
#     
#     datadash.create_bubble_filled_with_default("Process lifecycle phase", "Process analysis type", include={'process analysis'}, default_facet2_value='n/a')
    
    
#     domain_df=data_df.get_multivalued_column("Domain")
#     domain_df.to_csv(DOMAIN_FILE)
#     print(data_df.count_multivalued_column("Domain"))
#         
#     datadash.create_bar_count_multivalued_column("Domain",exclude=['undetermined'])
#     datadash.create_piechart_count_multivalued_column("Domain", exclude=['undetermined'])



#     logistic_coverage_df=data_df.get_multivalued_column("Logistics coverage")
#     logistic_coverage_df.to_csv(LOGISTIC_COVERAGE_FILE)
#     print(data_df.count_multivalued_column("Logistics coverage"))
#      
#     dict_log_cov_translation={'use case':'Use Case',\
#                               'motivating/running example':'Run. Ex.',\
#                               'general mention in the paper':'Gen. Men.',\
#                               'full':'Full',\
#                               'undetermined':'Undet.'
#                       }
#     datadash.create_bar_count_multivalued_column("Logistics coverage", rotation=45,translation=dict_log_cov_translation)
#     datadash.create_piechart_count_multivalued_column("Logistics coverage")
# 
    challenge_df=data_df.get_multivalued_column("challenge")
    challenge_df.to_csv(CHALLENGE_FILE)
    challenge_count_df= data_df.count_multivalued_column("challenge")
    print('index', challenge_count_df.index)
    challenge_count_df.to_csv("../out/challenge_count.csv")
    dict_translation={'event models for BPM':'CH01',\
                       'compliance& audit& privacy& security': 'CH02',\
                       'automatic event-based monitoring of processes' : 'CH03',\
                       'patterns and models for communication':'CH04',\
                       'choreographies&inter-process correlation':'CH05',\
                       'abstraction levels':'CH06',\
                       'context in events and processes':'CH07',\
                       'integrated platforms for BPM & CEP':'CH08',\
                       '(highly) distributed processes & the role of events':'CH09',\
                       'optimisation opportunities':'CH10',\
                       'event data quality':'CH11',\
                       'from event streams to process models and back':'CH12',\
                       'other':'CH13',\
                       'undetermined':'undetermined'
                       }   
    datadash.create_bar_count_multivalued_column("challenge", translation=dict_translation)
    datadash.create_piechart_count_multivalued_column("challenge", translation=dict_translation)
#     

#     
    
#     df=publ.get_ordered_studies
#     df.to_csv("../out/ordered_publications.csv")
    
#     v = venues.get_venue(103)
#     print(type(v), v)
#     v = venues.get_venue(4444)
#     print(type(v), v)
#     print("1--",dblat)
#     dblat.set_venues(venues)
#     print("2--",dblat)
#     dblat.generate_studies() 


#     focus_df=data_df.get_single_column("Focus")
#     focus_df.to_csv(FOCUS_FILE)
#     print(data_df.count_single_column("Focus"))
#     
#     model_lang_df=data_df.get_single_column("Modelling language")
#     model_lang_df.to_csv(MOD_LANG_FILE)
#     print(data_df.count_single_column("Modelling language"))
#     
#     model_lang_type_df=data_df.get_multivalued_column("Modelling language type")
#     model_lang_type_df.to_csv(MOD_LANG_TYPE_FILE)
#     print(data_df.count_multivalued_column("Modelling language type"))
# 
#     event_producer_df=data_df.get_multivalued_column("Technology of event producer")
#     event_producer_df.to_csv(EVENT_PRODUCER_FILE)
#     print(data_df.count_multivalued_column("Technology of event producer"))
#     
#     event_lang_df=data_df.get_single_column("Event processing Language")
#     event_lang_df.to_csv(EVENT_LANGUAGE_FILE)
#     count_event_lang_df = data_df.count_single_column("Event processing Language") 
#     count_event_lang_df.to_csv("../out/count_event_lang.csv")

      
# 
#     model_event_df=data_df.get_single_column("Model event")
#     model_event_df.to_csv(EVENT_MODEL_FILE)
#     print(data_df.count_single_column("Model event"))    

    keyword_df = publ.get_keywords_dataframe
    print(keyword_df)
    keyword_df.to_csv(KEYWORDS_FILE)
    keywords_dict=publ.get_keywords_per_study
    for key, value in sorted(keywords_dict.items()):
        print(key,"-->",value)
        
    
    keycl = keyclus.KeywordClusterer.of(list(keywords_dict.keys()))
    print(keycl.predict())
    print ('Number of clusters', keycl.get_number_of_clusters)
    print ('Labels ', keycl.get_labels )
    print ('X ', keycl.get_X)
    cluster_df=keycl.get_prediction()
    cluster_df.to_csv("../out/cluster.csv")
    cluster_df.reset_index(level=0, inplace=True)
    dic_clus=create_dict_from_single_column (cluster_df)
    for k,v in sorted(dic_clus.items()):
        print (k, '-->',v)