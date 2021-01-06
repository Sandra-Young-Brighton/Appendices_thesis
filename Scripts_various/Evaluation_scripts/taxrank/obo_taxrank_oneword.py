#convert obo file into pandas dataframe then .csv edge list for cytoscape

import pandas as pd
import os
import re
import csv


def del_firstword():
    names_df = pd.read_csv('vto_taxrank_dict.csv')
    
    #remove trailing whitespace
    names_df.columns.str.strip()
    print(names_df.head())
    
    #for two word names, create a column for the second word
    names_df['target'] = names_df['name'].str.split(' ').str[2]
    
    #for one word names, copy across from original name column
    names_df.loc[names_df['target'].isnull(), 'target'] = names_df['name']
    
    #rename the is_a column as source for ease in cytoscape usse directed relations
    names.df['is_a'] = names.df['source']
    
    #replace taxrank with correct rank as string
    
    print(names_df.head(30))
    
    clean_file = names_df.to_csv('vto_target.csv')

def main():
    path = './obo/'
    #file_clean(path)
    #file_convert(path)
    del_firstword()
    
if __name__ == '__main__':
    main ()