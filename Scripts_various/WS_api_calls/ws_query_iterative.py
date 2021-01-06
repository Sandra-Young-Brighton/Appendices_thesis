#!/usr/bin/python
import time
import requests
import os
import json


def sep_names():
    genup = []
    genera = []
    species = []
    subspecies = []
    file = open('names_lists.txt')
    for line in file:
        row = line.split(' ')  
        if len(row) == 1:
            genup.append(row[0])
        if len(row) == 2:
            genera.append(row[0])
            species.append(row[1])
        if len(row) == 3:
            genera.append(row[0])
            species.append(row[1])
            subspecies.append(row[2])
        else:
            continue
    print(genup)
    print(genera)
    print(species)
    print(subspecies)
    return genera, genup, species, subspecies



def main():

    #import names from corpus to be called as WS
    mult_list = sep_names()
    
    base_url = 'https://api.sketchengine.co.uk/bonito/run.cgi'
    url = 'https://api.sketchengine.co.uk/bonito/run.cgi/savews'
    data = {
        'corpname': 'user/sandrayoung/jeff_large_newbreakdown',
        'saveformat': 'xml',
        #'lpos': '-n',
        # get your API key here: https://the.sketchengine.co.uk/auth/api_access/
        'username': 'sandrayoung',
        'api_key': 'Q4CSB38CW5GEKZ7WP8RTRLOQIUEFAGKD',
        #'lemma': 'salmon',
        }
    for list in mult_list:
        for item in list:
            data['lemma'] = item
            #get the word sketch for said lemma
            response = requests.get(url, params=data)
            file = open(item+'.xml', 'w')#when do multiple title will be with item
            with file as f:
                f.write(response.text)
            # beware of FUP, see https://www.sketchengine.eu/service-level-agreement/
            time.sleep(10)

if __name__ == "__main__":
    main()