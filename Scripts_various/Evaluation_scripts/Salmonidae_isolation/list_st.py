#script to separate VTO Salmonidae dataframe into a list with all separate parts to search WS API

import pandas as pd
import os
from numpy.lib.utils import source

def list_sourcetarget(input_file, output_file):
    #read in df
    df_vto = pd.read_csv(input_file)
    #create lists for source and target columns and join and delete duplicates
    target_list = df_vto['target'].tolist()
    source_list = df_vto['source'].tolist()
    print('1:', target_list)
    print('2:', source_list)
    
    source_target = list(set(source_list + target_list))
    print('3:', source_target)
    
    #create text file with this list
    outfile = open(output_file, 'w')
    for item in source_target:
        outfile.write(item+'\n')
        

def main():
    list_sourcetarget('VTO_salmonidae_190619.csv', 'salmonidaelist_VTO.txt')
    
if __name__ == "__main__":
    main()