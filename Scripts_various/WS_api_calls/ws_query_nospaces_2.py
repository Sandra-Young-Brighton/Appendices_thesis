#!/usr/bin/python
import time
import requests
import os
import json
from _regex_core import name


def import_names(names_list):
    """Loads text file and turns into a list
    """
    file = open(names_list)
    orig_names = []
    for line in file:
        line = line.strip('\n')
        line = line.strip('\r')
        line = line.strip(' ')
        orig_names.append(line)

    names_nospace = []
    for name in orig_names:
        new_name = name.replace(" ", "_")
        names_nospace.append(new_name)
    
    return names_nospace


def main():

    #import names from corpus to be called as WS
    list = import_names('names_oncorhynchus_mykiss.txt')
    
    
    base_url = 'https://api.sketchengine.co.uk/bonito/run.cgi'
    url = 'https://api.sketchengine.co.uk/bonito/run.cgi/savews'
    data = {
        'corpname': 'user/sandrayoung/jeff_swu_oncmy',
        'saveformat': 'xml',
        #'lpos': '-n',
        # get your API key here: https://the.sketchengine.co.uk/auth/api_access/
        'username': 'sandrayoung',
        'api_key': 'Q4CSB38CW5GEKZ7WP8RTRLOQIUEFAGKD',
        #'lemma': 'salmon',
        }
#     i = 1
#     while i<=2000:
#         
     
    for i in range(0,min(2000,len(list))):
         item = list[i]
        
         name = item.strip()
         data['lemma'] = name
         #get the word sketch for said lemma
         response = requests.get(url, params=data)
         path = './JEFF_SWU_oncmy/'
         file = open(path+name+'.xml', 'w')#when do multiple title will be with item
         with file as f:
             f.write(response.text)
         # beware of FUP, see https://www.sketchengine.eu/service-level-agreement/
         time.sleep(2)   
         print(name)



                


if __name__ == "__main__":
    main()