"""
This file contains python functions for automatically retreiving DOI metadata
and creating bibtex references. `get_bibtex_entry(doi)` creates a bibtex entry
for a DOI. It fixes a Data Cite author name parsing issue. Short DOIs are used
for bibtex citation keys.
Created by Daniel Himmelstein and released under CC0 1.0.
Modified by reinaqu
"""

import urllib.request

import requests
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase

def shorten(doi:str, cache:dict={}, verbose:bool=False)->str:
    """
    Get the shortDOI for a DOI. Providing a cache dictionary will prevent
    multiple API requests for the same DOI.
    """
    if doi in cache:
        return cache[doi]
    quoted_doi = urllib.request.quote(doi)
    url = 'http://shortdoi.org/{}?format=json'.format(quoted_doi)
    try:
        response = requests.get(url).json()
        short_doi = response['ShortDOI']
    except Exception as e:
        if verbose:
            print(doi, 'failed with', e)
        return None
    cache[doi] = short_doi
    return short_doi

def get_bibtext(doi:str, cache:dict={})->str:
    """
    Use DOI Content Negotioation (http://crosscite.org/cn/) to retrieve a string
    with the bibtex entry. Providing a cache dictionary will prevent multiple
    API requests for the same DOI.
    """
    if doi in cache:
        return cache[doi]
    url = 'https://doi.org/' + urllib.request.quote(doi)
    header = {
        'Accept': 'application/x-bibtex',
    }
    response = requests.get(url, headers=header)
    bibtext = response.text
    if bibtext:
        cache[doi] = bibtext
    return bibtext

def get_bibtex_entry(doi:str, id:str=None,bibtext_cache:dict={}, shortdoi_cache:dict={})->dict:
    """
    Return a bibtexparser entry for a DOI
    """
    bibtext = get_bibtext(doi, cache = bibtext_cache)
    if not bibtext:
        return None

    parser = BibTexParser()
    parser.ignore_nonstandard_types = False
    bibdb = bibtexparser.loads(bibtext, parser)
    print (doi, '***', bibtext, len(bibdb.entries))
    entry= None
    if (len(bibdb.entries)>0):
        entry, = bibdb.entries
        quoted_doi = urllib.request.quote(doi)
        entry['link'] = 'https://doi.org/{}'.format(quoted_doi)
        if 'author' in entry:
            entry['author'] = ' and '.join(entry['author'].rstrip(';').split('; '))
            if id == None:
                short_doi = shorten(doi, cache = shortdoi_cache)
                entry['ID'] = short_doi[3:]
            else:
                entry['ID'] = id
    return entry

def entries_to_str(entries:dict)->str:
    """
    Pass a list of bibtexparser entries and return a bibtex formatted string.
    """
    db = BibDatabase()
    db.entries = entries
    return bibtexparser.dumps(db)

def entries_to_bibdb(entries:dict)->BibDatabase:
    """
    Pass a list of bibtexparser entries and return a bibtex formatted string.
    """
    db = BibDatabase()
    db.entries = entries
    return db

def normalize_doi(doi:str)->str:
    '''
    Receives a doi and return a normalized doi. 
    A normalized doi is a doi that do not starts with https://doi.org/ nor http://dx.doi.org/
    Examples:
        http://dx.doi.org/10.1016/j.jss.2013.07.024 returns 10.1016/j.jss.2013.07.024
        https://doi.org/10.1016/j.knosys.2019.05.024 returns  10.1016/j.knosys.2019.05.024
        10.1145/2675743.2771826 returns 10.1145/2675743.2771826
    '''
    normalized_doi = None
    if doi!=None and isinstance(doi,str):
        normalized_doi = doi.replace('https://doi.org/','')
        normalized_doi = normalized_doi.replace('http://dx.doi.org/','')
        normalized_doi = normalized_doi.replace('DOI','').strip().lower()
    return normalized_doi


if __name__=="__main__":
    e = get_bibtex_entry('10.1145/2675743.2771826')
    print(e)