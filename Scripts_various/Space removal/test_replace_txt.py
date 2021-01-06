"""Script to replace MWU names with the same without spaces for further analysis
"""
"""
Created on 22 Jan 2019
by Sandra
"""

import os
import json
from re import sub

def import_names():
    """Loads text file and turns into a list
    """
    path = './input/'
    filelist = os.listdir(path)
    sci = []
    for file in filelist:
        with open(path+file, 'r') as gnrd_file:
            gnrd_names = json.load(gnrd_file)
        
            for name in gnrd_names['names']:
                sci.append(name['scientificName'])
    return list(set(sci))

def names_wo_spaces():
    #create a dictionary of original names and names with no spaces to replace them
    orig_names = import_names()
    names_nospace = []
    for name in orig_names:
        name = name.split()
        if len(name) == 1:
            name = "_".join(name)
            names_nospace.append(name)
        if len(name) == 2:
            name = "_".join(name)
            names_nospace.append(name)
        if len(name) == 3:
            species = "_".join(name[1:])
            genus = "".join(name[0])
            new_name = genus+"_"+species
            print(new_name)
            names_nospace.append(new_name)
        if len(name) == 4:
            species = "_".join(name[1:])
            genus = "".join(name[0])
            new_name = genus+"_"+species
            print(new_name)
            names_nospace.append(new_name)
    print(names_nospace)
    names_dict = dict(zip(orig_names, names_nospace))
    print(str(names_dict))
    return names_dict

def replace_names(target, names_dict):
    for old, new in list(names_dict.items()):
        target = target.replace(old, new)
    #print(target)
    return target
        
def main():
    path = './jeff_in/'
    filelist = os.listdir(path)
    names_dict = names_wo_spaces()
    for filename in filelist:
        file = open(path+filename, 'r').read()
        path2 = './jeff_nospace_oncmy/'
        output = replace_names(file, names_dict)
        filename, file_extension = os.path.splitext(filename)
        f = open(path2+filename+'_nospaces.txt', 'w')                   #what file you want to write to
        f.write(output)                                       #write to the file
        #print(output)       

if __name__ == '__main__':
    main ()
