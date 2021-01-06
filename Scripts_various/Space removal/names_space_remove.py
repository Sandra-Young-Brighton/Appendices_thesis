#!/usr/bin/python
import os
import json
from _regex_core import name

def import_names(path, names_list):
    """Loads text file and turns into a list
    """
    file = open(path+names_list)
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
    
    path = './oncmy_lists/'
    filelist = os.listdir(path)
    
    for file in filelist:
        names = import_names(path, file)
        no_path = os.path.basename(file)
        filename = os.path.splitext(no_path)
        (f,ext) = filename
        outfile = open(path+f+'_no_spaces.txt', 'w+')
        for name in names:
            outfile.write(name+'\n')

                


if __name__ == "__main__":
    main()