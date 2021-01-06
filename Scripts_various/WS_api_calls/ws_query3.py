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
    mult_list = set(genup+genera+species+subspecies)
    print(mult_list)
    return mult_list



def main():

    #import names from corpus to be called as WS
    mult_list = sep_names()
    path = './'
    filelist = os.listdir(path)
    new_list = []
    for name in mult_list:
        if name not in filelist:
            new_list.append(name)
    print(new_list)
    print(len(new_list))        
    
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
    for i in range(0,min(2000(len(multi_list)))):
        item = list[i]
        data['lemma'] = item
        #get the word sketch for said lemma
        response = requests.get(url, params=data)
        file = open(item+'.xml', 'w')#when do multiple title will be with item
        with file as f:
            f.write(response.text)
            # beware of FUP, see https://www.sketchengine.eu/service-level-agreement/
            time.sleep(2)
            #add one to i
            i+=1
            #print names completed to text file
            out_file = open('names_complete_1.txt', 'a')
            out_file.write(str(item)+'\n')
                 
if __name__ == "__main__":
    main()