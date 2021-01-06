#convert the taxrank to dictionary and replace the taxrank ID with rank word in VTO file

import pandas as pd
import os
import numpy as np
import re
import csv

def file_clean():
    with open('vto_taxrank.obo', 'r') as file:
        lines = file.readlines()
        keep = ['id: ', 'name: ']
        term = '[Term]'
    with open('vto_taxrank.txt', 'w') as clean_file:
        for line in lines:
                if any(item in line for item in keep):
                    line = line.strip('\n')
                    clean_file.write(line + '~')
                elif term in line:
                    clean_file.write('\n')
                else: 
                    continue
                    
                
def file_convert():
    with open('vto_taxrank.txt', 'r') as clean_file:
        lines = clean_file.readlines()
        dictList = []
        lines_clean = []
        for line in lines:
            if line == '\n':
                continue
            else:
                lines_clean.append(line)
        #print(lines_clean)        
        for line in lines_clean:
            #remove any dangling whitespace from line
            line = line.strip()
            #split line by ~
            list = line.split('~')
            #print(list)
            #create a list to turn into a dictionary of the names and rank ids
            dictTerm = {}
            rank = re.compile('id: TAXRANK:')
            
            dictTermList = []
            for item in list:
                if item == '':
                    #need to figure out how to delete this
                    continue
                elif re.search(rank, item):
                    if True:
                        item = item[4:]
                        print(item)
                        dictTermList.append(item)
                    else: 
                        continue
                elif 'name: ' in item:
                    print(item)
                    dictTermList.append(item)
                try:
                    dictTerm = {k:v for k, v in (x.split(':') for x in dictTermList)}
                    #print(dictTerm)
                except:
                    print(dictTermList)
                    exc_entries = open('taxrank_excl_entries.txt', 'a')
                    exc_entries.write(str(dictTermList) +'\n')
            dictList.append(dictTerm)
            
            print(dictList)
            taxrankList = []
            nameList = []
            for item in dictList:
                taxrank = item['TAXRANK']
                name = item['name']
                taxrankList.append(taxrank)
                nameList.append(name)
            print(taxrankList)
            print(nameList)
            taxrankDict = dict(zip(taxrankList, nameList))
            print(taxrankDict)               
    return taxrankDict
        
def replace(vto_file,taxrank_dict):
    #read in dataframe and dictionary
    vto_file = open(vto_file, 'r')
    lines = vto_file.readlines()
    taxrank_dict = taxrank_dict
    vto_file_new = open('vto_taxrank_names.csv', 'w')
    vto_file_new.write('name,TAXRANK,is_a\n')
    for line in lines:
            for key in taxrank_dict.keys():
                value = taxrank_dict[key]
                if key in line:
                    new_line = line.replace(key, value)
                    vto_file_new.write(new_line)
                else:
                    continue
                 
def main():

    file_clean()
    taxrank_dict = file_convert()
    replace('vto_clean_dict.txt', taxrank_dict)

    
if __name__ == "__main__":
    main()