# -*- coding: utf-8 -*-
'''
Created on 27 may. 2020

@author: reinaqu_2
'''
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
import bibtexparser
import os.path
import sys
from collections import Counter

def load_bibtex(filename):
   
    if not (os.path.isfile(filename)):
        print("input file not found"+ filename, file=sys.stderr)
        exit(0)
        
    parser = BibTexParser(common_strings=True) 
    with open(filename,encoding='utf-8') as bibtex_file:
        database = bibtexparser.load(bibtex_file, parser)
    return database 

def load_bibtex_as_text(filename):
    
    if not (os.path.isfile(filename)):
        print("input file not found"+ filename, file=sys.stderr)
        exit(0)
        
    with open(filename,  encoding='utf-8') as bibtex_file:
        data = bibtex_file.read() #read the whole file in a str
    return data


def load_bibtexs(filenames):
    ''' Get a sequence of filenames and returns a list of databases one for each filename.
        If any of the files do not exists, the process finishes.
    '''
    return [load_bibtex(filename) for filename in filenames]

def write_bibtex(db, filename):
    '''
    Writes the database into the file named filename
    '''
    with open(filename, 'w', encoding='utf-8') as bibtex_file:
        writer = BibTexWriter()
        writer.add_trailing_comma = True
        writer.indent=''
        bibtexparser.dump(db, bibtex_file,writer)

def writes_bibtex(db):
    '''
    Returns a string with the bibtex of the entries contained in the database
    '''
    return bibtexparser.dumps(db)

def write_bibtex_as_text(filename,data):
    '''
    Writes the database into the file named filename
    '''
    with open(filename, 'w', encoding='utf-8') as bibtex_file:
        bibtex_file.write(data)

def merge_dbs (db_list):
    res = BibDatabase()
    for db in db_list:
        for entry in db.entries:
            res.entries.append(entry)       
    return res

def subtract_dbs(db_min, list_dbs_sub):
    """
    The result of the operation is db_min -  union (db_sub_list).
    The result is the db_min without the references included in the list_dbs_sub databases 
    """
    db_subs = merge_dbs(list_dbs_sub)
    db = BibDatabase()
    for entry in db_min.entries:
        if not contains(entry, db_subs):
            db.entries.append(entry)
    return db

def contains(entry, database):
    """
    check if entry exits in the database, based on its ID
    """
    for ent in database.entries:
        if entry['ID'] == ent['ID']:
            return True
    return False

def count_entries_by_type(entries):
    types = [entry['ENTRYTYPE'] for entry in entries]
    return Counter(types)

def get_entries_ids(entries):
    return {entry['ID'] for entry in entries}

def common_entries (db1, db2):
    ids1 = get_entries_ids(db1.get_entry_list())
    ids2 = get_entries_ids(db2.get_entry_list())
    intersect = ids1 & ids2
    return intersect

def print_database_stats(database):
    entries = database.get_entry_list()
    print ("Number of entries:" , len(entries))
    print ("Entries per type:" , count_entries_by_type(entries))
