#convert obo taxrank file into pandas dataframe the .csv file to use to replace ID with rank name in the VTO edge list

import pandas
import networkx
import os
import re
import csv
from _regex_core import name

def file_clean(path):
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
                    
                
def file_convert(path):
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

                
        headers = ['name','TAXRANK']
        with open('vto_taxrank_dict.csv', 'w') as csv_file:
            dict_writer = csv.DictWriter(csv_file, headers)
            dict_writer.writeheader()
            try:
                dict_writer.writerows(dictList)
            except ValueError as e:
                print(e)
                #continue

def main():
    path = './obo/'
    file_clean(path)
    file_convert(path)

if __name__ == '__main__':
    main ()