# -*- coding: utf-8 -*-
'''
Created on 14 jul. 2021

@author: reinaqu_2
'''
import json

def write_json(d: dict, filename):
    json_object = json.dumps(d, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def read_json(filename):
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
    except ValueError as err:
            data ={}  
    except FileNotFoundError as err: 
            data ={}    
    return data

def to_json(o: object):
    return json.dumps(o,default=lambda x: x.__dict__, indent=4)

def json_decode(str_json:str):
    return json.loads(str_json)

    
if __name__=="__main__":
    data = read_json("file.json")
    print(data.keys())