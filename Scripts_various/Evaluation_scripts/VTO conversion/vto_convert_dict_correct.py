#convert obo file into pandas dataframe then .csv edge list for cytoscape

import pandas
import networkx
import os
import re
import csv

def file_clean(path):
    with open('vto.obo', 'r') as file:
        lines = file.readlines()
        keep = ['name: ', 'is_a: ', 'property_value: ']
        term = '[Term]'
    with open('vto_clean_3.txt', 'w') as clean_file:
        for line in lines:
                if any(item in line for item in keep):
                    line = line.strip('\n')
                    clean_file.write(line + '~')
                elif term in line:
                    clean_file.write('\n')
                else: 
                    continue
                    
                
def file_convert(path):
    with open('vto_clean_3.txt', 'r') as clean_file:
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
            #dictTerm = {k:v for k, v in (x.split(':') for x in list)}
            #print(dictTerm)
            #list = list[0:3]
            #print(list)
            #print(len(list))
            dictTerm = {}
            rank = re.compile('property_value: has_rank ')
            #is_a = re.compile(' VTO:\w{6,8} !')
            dictTermList = []
            for item in list:
                if 'boolean' in item:
                    continue
                elif item == '':
                    #need to figure out how to delete this
                    continue
                elif re.search(rank, item):
                    if True:
                        item = item[25:]
                        #print(rank_item)
                        dictTermList.append(item)
                    else: 
                        continue
                elif 'is_a: ' in item:
                    is_a = item[0:5] + item[19:]
                    #print(is_a)
                    dictTermList.append(is_a)
                else:
                    dictTermList.append(item)
                #print(dictTermList)
                try:
                    dictTerm = {k:v for k, v in (x.split(':') for x in dictTermList)}
                    #print(dictTerm)
                except:
                    print(dictTermList)
            dictList.append(dictTerm)
            
            #print(dictList)
        
        headers = ['name','TAXRANK', 'is_a']
        with open('vto_clean_dict.csv', 'w') as csv_file:
            dict_writer = csv.DictWriter(csv_file, headers)
            dict_writer.writeheader()
            try:
                dict_writer.writerows(dictList)
            except ValueError as e:
                print(e)
                

                

def main():
    path = './obo/'
    file_clean(path)
    file_convert(path)

if __name__ == '__main__':
    main ()