#compare the edges lists of VTO versus the data

import pandas as pd
import os
import numpy as np

def multiple_appends(listname, *element):
    listname.extend(element)

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
	df_jeff_vto_match = df_jeff_vto_match.drop_duplicates()
     
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
    df_vto_ind = float(len(df_vto.index))
    print('1:', df_vto_ind)
    df_jeff_ind = float(len(df_jeff.index))
    print('2:', df_jeff_ind)
    vto_only_ind = float(len(vto_only.index))
    print('3:', vto_only_ind)
    jeff_only_ind = float(len(jeff_only.index))
    print('4:', jeff_only_ind)
    in_both_ind = float(len(df_jeff_vto_match.index))
    print('5:', in_both_ind)
    #% just in VTO
    pcent_vto = (vto_only_ind/df_vto_ind)*100
    print('6:', pcent_vto)
      
    #%common
    pcent_both_vto = (in_both_ind/df_vto_ind)*100
    print('7:', pcent_both_vto)
    pcent_both_jeff = (in_both_ind/df_jeff_ind)*100
    print('8:', pcent_both_jeff)
    #% just in JEFF
    pcent_jeff = (jeff_only_ind/df_jeff_ind)*100
    print('9:', pcent_jeff)
    
    #make list of items in order
    list = []
    multiple_appends(list,jeff_file, df_vto_ind, df_jeff_ind, vto_only_ind, jeff_only_ind, in_both_ind, pcent_vto, pcent_jeff, pcent_both_vto, pcent_both_jeff)

    print(len(list))
    return list

#     with open(output_path+'comparison_percentages_VTOsalm.txt', 'a') as file:
#         file.write(jeff_file+' in comparison with'+ vto_file + '\n')
#         
#         file.write('VTO total :' +(str(df_vto_ind))+'\n')
#         file.write('JEFF total : '+ (str(df_jeff_ind))+'\n')
#         file.write('VTO not in JEFF: '+ (str(vto_only_ind))+'\n')
#         file.write('JEFF not in VTO: ' + (str(jeff_only_ind))+'\n')
#         file.write('VTO in JEFF: ' + (str(in_both_ind))+'\n')
#          
#         file.write('Percentage only in VTO: ' + str(pcent_vto) +'\n')
#         file.write('Percentage only in JEFF: ' + str(pcent_jeff) +'\n')
#         file.write('Percentage common compared to VTO: ' + str(pcent_both_vto) +'\n')
#         file.write('Percentage common compared to JEFF: ' + str(pcent_both_jeff) +'\n\n')   
#                     
def main():
    input_path = './input_JEFF_scionly/'
    output_path = './output_sourcetarget_JEFFsci/'
    
    filelist = os.listdir(input_path)
    i = 1
    df = pd.DataFrame()
    
    # read in files as dataframe and change to lists
    for jeff_file in filelist:
        if jeff_file.endswith('csv'):         
            list = compare('vto_taxrank_sourcetarget_190619.csv', input_path, jeff_file, output_path)
            #printing to a file with the percentages
            df = df.append(pd.DataFrame([list], columns=('filter', 'VTO_total', 'JEFF_total', 'VTO_not_in_JEFF', 'JEFF_not_in_VTO', 'VTO_in_JEFF', '%_only_in_JEFF', '%_only_in_VTO', '%_common_vs_VTO','%_common_JEFF')))
    
    df.to_csv(output_path + 'comparison_percentages_JEFFall.csv', index=False)
    
if __name__ == "__main__":
    main()