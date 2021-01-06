#search through vto for nodes and add the ranking to the jeff nodes for evaluation purposes
import pandas as pd
import os
import csv

def rank_add(vto_file, input_path, jeff_file, output_path):
#read in the vto file and the jeff file as dataframes
    df_vto = pd.read_csv(vto_file)
    df_jeff = pd.read_csv(input_path+jeff_file)

#remove unnecessary columns (jeff dataframe is the one with just nodes (look at the jeff oneand sort out)
    df_vto = df_vto.drop('name', axis=1)
    df_vto = df_vto.drop('is_a', axis=1)
    #df_vto = df_vto.drop('source', axis=1)
    #df_jeff_new = df_jeff.filter(['name', 'ClosenessCentrality', 'NeighborhoodConnectivity'], axis=1)
    
#rename jeff dataframe with target node
    df_jeff = df_jeff.rename(columns={'child': 'target', 'parent': 'source'})
 
#all upper
    df_vto = df_vto.apply(lambda x: x.astype(str).str.upper())
    df_vto = df_vto.reset_index(drop=True)
    df_vto['source'] = df_vto['source'].str.strip()
    df_vto['target'] = df_vto['target'].str.strip()
    df_vto = df_vto.filter(['TAXRANK_target', 'target', 'TAXRANK_source', 'source'], axis=1)
    print(df_vto)

#reset index and prepare for filename     
    df_jeff_new = df_jeff.reset_index(drop=True)

    no_path = os.path.basename(jeff_file)
    filename = os.path.splitext(no_path)
    (f, ext) = filename
    
    print(df_jeff_new)

#search for target in JEFF and VTO - if match taxrank in vto = taxrank in jeff
    df_jeff_vto_match = pd.merge(df_jeff_new, df_vto, how='inner', on=['source', 'target'])
    print(df_jeff_vto_match)
    #df_vto_match = df_vto[(df_vto['source'].isin(df_jeff_new['source']) & df_vto['target'].isin(df_jeff_new['target']))].dropna().reset_index(drop=True)
    #print(df_vto_match)
    #make a dataframe with all jeff, whether ranked or not
    df_jeff_rank_all = df_vto.merge(df_jeff_new.drop_duplicates(), on=['source', 'target'], how='right', indicator=True)
    print(df_jeff_rank_all)
    #df_jeff_rank = pd.merge(df_vto_match, df_jeff_match, on='target')
    df_jeff_rank = df_jeff_vto_match.reset_index(drop=True)
    print(df_jeff_rank)
    
    df_jeff_rank_all = df_jeff_rank_all.reset_index(drop=True)
    
    #print to file
    df_jeff_rank.to_csv(output_path+'jeff_rank_actual'+f+'.csv', index=False)
    
    df_jeff_rank_all.to_csv(output_path+'jeff_rank_all'+f+'.csv', index=False)


def main():
    input_path = './input_files/'
    output_path = './jeff_sourcetarget_ranks/'
    
    filelist = os.listdir(input_path)
    i = 1
    # read in files as dataframe and change to lists
    for jeff_file in filelist:
        if jeff_file.endswith('csv'):         
            rank_add('vto_taxrank_sourcetarget.csv', input_path, jeff_file, output_path)
    
if __name__ == '__main__':
    main ()