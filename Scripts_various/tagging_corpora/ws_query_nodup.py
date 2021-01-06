#!/usr/bin/python
import time
import requests
import os
import json


def mult_list():
    genup = []
    genera = []
    species = []
    subspecies = []
    file = open('names_list_nospace.txt')
    for line in file:
        row = line.strip().split(' ')
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
    mult_list = list(set(genera + genup + species + subspecies))
    print(len(set(mult_list)))
    return mult_list

def delete_names(path, filelist, list):
    filenames = []
    for file in filelist:
        file = file.strip('.xml')
        filenames.append(file)
        
    mult_list = [name for name in list if name not in filenames]
    print(len(mult_list))
    print(mult_list)
    return mult_list
        

def main():
    path = './jeff_nospaces_WS/'
    #make a list of existing filenames    
    filelist = os.listdir(path)
    #read in file to create list
    list = mult_list()
    #delete names from original file
    noduplist = delete_names(path, filelist, list)

    base_url = 'https://api.sketchengine.co.uk/bonito/run.cgi'
    url = 'https://api.sketchengine.co.uk/bonito/run.cgi/savews'
    data = {
        'corpname': 'user/sandrayoung/jeff_nospaces_tagged',
        'saveformat': 'xml',
        #'lpos': '-n',
        # get your API key here: https://the.sketchengine.co.uk/auth/api_access/
        'username': 'sandrayoung',
        'api_key': 'Q4CSB38CW5GEKZ7WP8RTRLOQIUEFAGKD',
        #'lemma': 'salmon',
        }
      
    for i in range(0, min(2000, len(noduplist))):
        item = noduplist[i]

        name = item.strip()
        data['lemma'] = name
        #get the word sketch for said lemma
        response = requests.get(url, params=data)
        file = open(path+item+'.xml', 'w')#when do multiple title will be with item
        with file as f:
            f.write(response.text)
        # beware of FUP, see https://www.sketchengine.eu/service-level-agreement/
        time.sleep(2)
        print(item)
 
if __name__ == "__main__":
    main()