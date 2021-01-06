#compare the edges lists of VTO versus the data

import pandas as pd
import os
import numpy as np

def compare(vto_file, input_path, jeff_file, output_path):
    #read in both dataframes
    df_vto = pd.read_csv(vto_file)
    df_jeff = pd.read_csv(input_path+jeff_file)
    
    #remove unnecessary columns for now
    df_vto = df_vto.drop('name', axis=1)
    df_vto = df_vto.drop('is_a', axis=1)
    #df_vto = df_vto.drop('TAXRANK', axis=1)
    df_jeff = df_jeff.drop('hits', axis=1)
    df_jeff = df_jeff.drop('score', axis=1)
    df_jeff = df_jeff.drop('score.1', axis=1)
    
    df_jeff = df_jeff.rename(columns={'parent': 'source', 'child': 'target'})
    
    
    #all upper
    df_vto = df_vto.apply(lambda x: x.astype(str).str.upper())
    df_vto = df_vto.reset_index(drop=True)
    df_vto['source'] = df_vto['source'].str.strip()
    df_vto['target'] = df_vto['target'].str.strip()
    #print(df_vto)
    
    #add columns to denote the datafame
    df_vto['data_source'] = 'VTO ontology'
    df_jeff['data_source'] = 'JEFF corpus' 
    
    df_vto['relations'] = 'is_a'
    
    print(df_vto)
    print(df_jeff)
    
    df_jeff = df_jeff.reset_index(drop=True)
    #df_jeff.index = df_jeff.index + 1   
    #df_vto.index = df_vto.index + 1 
    no_path = os.path.basename(jeff_file)
    filename = os.path.splitext(no_path)
    (f, ext) = filename
    
   
    #produce table with common items - this bit is working
    df_jeff_vto_match = pd.merge(df_jeff, df_vto, on=['source', 'target'], how='inner')
     
    #add the column
    df_jeff_vto_match['compare'] = 'both'
    print(df_jeff_vto_match)
    df_jeff_vto_match.to_csv(output_path+'vto_in_'+f+'.csv', index=False)
    
    #merge dataframes to get common and not common
    vto_all_jeff_common = df_vto.merge(df_jeff.drop_duplicates(), on=['source', 'target'], how='left', indicator=True)
    print(vto_all_jeff_common)
    vto_all_jeff_common.to_csv(output_path+'vto_all_jeff_common_'+f+'.csv', index=False)
    
    jeff_all_vto_common = df_vto.merge(df_jeff.drop_duplicates(), on=['source', 'target'], how='right', indicator=True)
    print(jeff_all_vto_common)
    jeff_all_vto_common.to_csv(output_path+'jeff_all_vto_common_'+f+'.csv', index=False)
    
    #vto_and_jeff 
    
    #vto_all_jeff_common['_merge'] == 'left_only'
    vto_only = vto_all_jeff_common[vto_all_jeff_common._merge == 'left_only']
    vto_only = vto_only.drop(columns=['data_source_y', 'relations_y', '_merge'], axis=1)
    #vto_only = vto_only.drop('left_only')
    vto_only.to_csv(output_path+'vto_only_'+f+'.csv', index=False)
    #print(vto_and_jeff)

    jeff_only = jeff_all_vto_common[jeff_all_vto_common._merge == 'right_only']
    jeff_only = jeff_only.drop(columns=['data_source_x', 'relations_x', '_merge'], axis=1)
    #'jeff_only = jeff_only.drop('right_only')
    jeff_only.to_csv(output_path+'jeff_only_'+f+'.csv', index=False)

  
    #% of common or otherwise 
    df_vto_ind = len(df_vto.index)
    print(df_vto_ind)
    df_jeff_ind = len(df_jeff.index)
    print(df_jeff_ind)
    vto_only_ind = len(vto_only.index)
    jeff_only_ind = len(jeff_only.index)
    in_both_ind = len(df_jeff_vto_match.index)
    #% just in VTO
    pcent_vto = (vto_only_ind/df_vto_ind)*100
      
    #%common
    pcent_both_vto = (in_both_ind/df_vto_ind)*100
    pcent_both_jeff = (in_both_ind/df_jeff_ind)*100
    #% just in JEFF
    pcent_jeff = (jeff_only_ind/df_jeff_ind)*100
      
    #printing to a file with the percentages   
  
      
    with open(output_path+'comparison_percentages.txt', 'a') as file:
        file.write(jeff_file+'\n')
        file.write('VTO total :' +(str(df_vto_ind))+'\n')
        file.write('JEFF total : '+ (str(df_jeff_ind))+'\n')
        file.write('VTO not in JEFF: '+ (str(vto_only_ind))+'\n')
        file.write('JEFF not in VTO: ' + (str(jeff_only_ind))+'\n')
        file.write('VTO in JEFF: ' + (str(in_both_ind))+'\n')
         
        file.write('Percentage only in VTO: ' + str(pcent_vto) +'\n')
        file.write('Percentage only in JEFF: ' + str(pcent_jeff) +'\n')
        file.write('Percentage common compared to VTO: ' + str(pcent_both_vto) +'\n')
        file.write('Percentage common compared to JEFF: ' + str(pcent_both_jeff) +'\n\n')   
#                     
def main():
    input_path = './input_JEFF_scionly/'
    output_path = './output_sourcetarget/'
    
    filelist = os.listdir(input_path)
    i = 1
    # read in files as dataframe and change to lists
    for jeff_file in filelist:
        if jeff_file.endswith('csv'):         
            compare('vto_taxrank_sourcetarget.csv', input_path, jeff_file, output_path)
    
if __name__ == "__main__":
    main()