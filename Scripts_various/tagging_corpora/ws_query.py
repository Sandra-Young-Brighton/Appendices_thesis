#!/usr/bin/python
import time
import requests
import os
import json


def import_names(path, filelist):
    """Loads json file and turns into a list
    """
    sci = []
    for file in filelist:
        with open(path+file, 'r') as gnrd_file:
            gnrd_names = json.load(gnrd_file)
        
            for name in gnrd_names['names']:
                sci.append(name['scientificName'])
    list_nodup = list(set(sci))
    names = open('names_list.txt', 'w')
    i = 1
    for item in list_nodup:
        names.write(str(i)+'|'+item+'\n')
        i+=1
    
    genup = []
    genera = []
    species = []
    subspecies = []
    for name in list_nodup:
        row = name.split(' ')
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

#list = ['salmo', 'oncorhynchus', 'trutta', 'salar']

def main():
    path = './output/'
    filelist = os.listdir(path)
    list = import_names(path, filelist)
    
    base_url = 'https://api.sketchengine.co.uk/bonito/run.cgi'
    url = 'https://api.sketchengine.co.uk/bonito/run.cgi/wsketch'
    data = {
        'corpname': 'user/sandrayoung/jeff_large',
        'format': 'json',
        #'lpos': '-n',
        # get your API key here: https://the.sketchengine.co.uk/auth/api_access/
        'username': 'sandrayoung',
        'api_key': 'Q4CSB38CW5GEKZ7WP8RTRLOQIUEFAGKD',
        }
    
    for item in list:
        data['lemma'] = item
        response = requests.get(url, params=data).json()
        file = open('wsketch_gen.json', 'a')
        with file as f:
            #f.write(item+':\n')
            f.write(str(response)+'\n')
            #gramrels = response['Gramrels']
            #f.write(str(gramrels))
        # beware of FUP, see https://www.sketchengine.eu/service-level-agreement/
        time.sleep(5)
        
if __name__ == "__main__":
    main()