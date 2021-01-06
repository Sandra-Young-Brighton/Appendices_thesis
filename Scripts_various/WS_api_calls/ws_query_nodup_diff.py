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
    file = open('names_lists.txt')
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
    
    list_diff = []
    for item in mult_list:
        ext = item + '_ext'
        jeff = item + '_JEFF'
        list_diff.append(ext)
        list_diff.append(jeff)
    print(list_diff)  
    return list_diff
 
def delete_names(path, filelist, list):
    filenames = []
    for file in filelist:
        file = file.strip('.xml')
        filenames.append(file)
         
    list_diff = [name for name in list if name not in filenames]
    print(len(list_diff))
    print(list_diff)
    return list_diff
        

def main():
    path = './jeffplusextended_diffall/'
    #make a list of existing filenames    
    filelist = os.listdir(path)
    #read in file to create list
    list = mult_list()
    #delete names from original file
    noduplist = delete_names(path, filelist, list)
    
    #list = ['goby', 'whitefish', 'chub', 'perch', 'trout', 'salmon', 'eel', 'stickleback',
            #'insect', 'species', 'specie', 'plant', 'fish', 'animal', 'plant', 'nymph', 'parr', 'larva', 'larvae', 'egg', 'eat,consume,feed' ]
     
    base_url = 'https://api.sketchengine.co.uk/bonito/run.cgi'
    url = 'https://api.sketchengine.co.uk/bonito/run.cgi/savews'
    data = {
        'corpname': 'user/sandrayoung/jeffplusextended_diffall',
        'saveformat': 'xml',
        #'lpos': '-n',
        # get your API key here: https://the.sketchengine.co.uk/auth/api_access/
        'username': 'sandrayoung',
        'api_key': 'Q4CSB38CW5GEKZ7WP8RTRLOQIUEFAGKD',
        #'lemma': 'salmon',
        }
      
    for i in range(0, min(5000, len(noduplist))):
        item = noduplist[i]
#     for i in range(0, min(5000, len(list))):
#         item = list[i]
        name = item.strip()
        data['lemma'] = name
        #get the word sketch for said lemma
        response = requests.get(url, params=data)
        file = open(path+item+'.xml', 'w')#when do multiple title will be with item
        with file as f:
            f.write(response.text)
        # beware of FUP, see https://www.sketchengine.eu/service-level-agreement/
        time.sleep(5)
        print(item)
 
if __name__ == "__main__":
    main()