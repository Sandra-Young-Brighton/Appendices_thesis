#compare the edges lists of VTO versus the data

import pandas as pd
import os
import numpy as np

def multiple_appends(listname, *element):
    listname.extend(element)

def compare(corp1_file, input_path, corp2_file, output_path):
	#for this just use the complete amount - it is to gain an idea of the comparability of the two corpora
	#should it be from the files compared with VTO so there are ranks for those which matched VTO?
    #read in both dataframes
    df_corp1 = pd.read_csv(input_path + corp1_file)
    df_corp2 = pd.read_csv(input_path + corp2_file)
    
    #remove unnecessary columns for now
    df_corp1 = df_corp1.drop(['data_source_x','relations_x','relations_y','data_source_y','_merge'], axis=1)
    df_corp2 = df_corp2.drop(['data_source_x','relations_x','relations_y','data_source_y','_merge'], axis=1)

    
    #all upper
    df_corp1 = df_corp1.apply(lambda x: x.astype(str).str.upper())
    df_corp1 = df_corp1.reset_index(drop=True)
	df_corp2 = df_corp2.apply(lambda x: x.astype(str).str.upper())
    df_corp2 = df_corp2.reset_index(drop=True)
    #df_vto['source'] = df_vto['source'].str.strip()
    #df_vto['target'] = df_vto['target'].str.strip()
    #print(df_vto)
    
    #add columns to denote the datafame
    df_corp1['data_source'] = 'JEFF corpus'
    df_corp2['data_source'] = 'extended corpus' 
    
    #df_vto['relations'] = 'is_a'
    
    print(df_corp1)
    print(df_corp2)
    
    #df_jeff = df_jeff.reset_index(drop=True)
    #df_jeff.index = df_jeff.index + 1   
    #df_vto.index = df_vto.index + 1 
    no_path = os.path.basename(jeff_file)
    filename = os.path.splitext(no_path)
    (f, ext) = filename
    
   
    #produce table with common items - this bit is working
    df_jeff_ext_match = pd.merge(df_corp1, df_corp2, on=['source', 'target'], how='inner')
     
    #add the column
    df_jeff_ext_match['compare'] = 'both'
    print(df_jeff_ext_match)
    df_jeff_ext_match.to_csv(output_path+'ext_in_'+f+'.csv', index=False)
    
    #merge dataframes to get common and not common
    ext_all_jeff_common = df_corp2.merge(df_corp1.drop_duplicates(), on=['source', 'target'], how='left', indicator=True)
    print(ext_all_jeff_common)
    ext_all_jeff_common.to_csv(output_path+'ext_all_jeff_common_'+f+'.csv', index=False)
    
    jeff_all_ext_common = df_corp2.merge(df_corp1.drop_duplicates(), on=['source', 'target'], how='right', indicator=True)
    print(jeff_all_ext_common)
    jeff_all_ext_common.to_csv(output_path+'jeff_all_ext_common_'+f+'.csv', index=False)
    
    #vto_and_jeff 
    
    #vto_all_jeff_common['_merge'] == 'left_only'
    ext_only = ext_all_jeff_common[ext_all_jeff_common._merge == 'left_only']
    ext_only = ext_only.drop(columns=['data_source_y', 'relations_y', '_merge'], axis=1)
    #vto_only = vto_only.drop('left_only')
    ext_only.to_csv(output_path+'vto_only_'+f+'.csv', index=False)
    #print(vto_and_jeff)

    jeff_only = jeff_all_ext_common[jeff_all_ext_common._merge == 'right_only']
    jeff_only = jeff_only.drop(columns=['data_source_x', 'relations_x', '_merge'], axis=1)
    #'jeff_only = jeff_only.drop('right_only')
    jeff_only.to_csv(output_path+'jeff_only_'+f+'.csv', index=False)

  
    #% of common or otherwise 
    df_corp2_ind = float(len(df_corp2.index))
    print('1:', df_corp2_ind)
    df_corp1_ind = float(len(df_corp1.index))
    print('2:', df_corp1_ind)
    corp2_only_ind = float(len(corp2_only.index))
    print('3:', corp2_only_ind)
    corp1_only_ind = float(len(corp1_only.index))
    print('4:', corp1_only_ind)
    in_both_ind = float(len(df_jeff_ext_match.index))
    print('5:', in_both_ind)
    #% just in VTO
    pcent_ext = (ext_only_ind/df_corp2_ind)*100
    print('6:', pcent_ext)
      
    #%common
    pcent_both_ext = (in_both_ind/df_corp2_ind)*100
    print('7:', pcent_both_ext)
    pcent_both_jeff = (in_both_ind/df_corp1_ind)*100
    print('8:', pcent_both_jeff)
    #% just in JEFF
    pcent_jeff = (jeff_only_ind/df_corp1_ind)*100
    print('9:', pcent_jeff)
    
    #make list of items in orde
	#need to sort out the file names to make it work
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