#compare the edges lists of VTO versus the data

import pandas as pd
import os
import numpy as np

def multiple_appends(listname, *element):
    listname.extend(element)

def compare(WEBfreq_file, input_path, WEBsal_file, output_path):
    #read in both dataframes
    df_WEBfreq = pd.read_csv(WEBfreq_file)
    df_WEBsal = pd.read_csv(input_path+WEBsal_file)
    
    print(df_WEBfreq)
    print(df_WEBsal)
    
    
    #change  columns to denote the datafame
    df_WEBsal.loc[:,'data_source'] = 'WEB salience'
    df_WEBfreq.loc[:, 'data_source'] = 'WEB frequency' 
    df_WEBsal.loc[:, '_merge'].replace('both', 'VTO match')
    df_WEBfreq.loc[:, '_merge'].replace('both', 'VTO match')
    df_WEBsal.loc[:, '_merge'].replace('right_only', 'WEB only')
    df_WEBfreq.loc[:, '_merge'].replace('right_only', 'WEB only') 
    
    df_WEBsal.rename(columns={'_merge': 'included'}, inplace=True)
    df_WEBfreq.rename(columns={'_merge': 'included'}, inplace=True)
    #drop unnecessary columns
    df_WEBsal.drop(['TAXRANK_target', 'TAXRANK_source', 'data_source_x', 'relations', 'data_source_y'], axis=1)
    df_WEBfreq.drop(['TAXRANK_target', 'TAXRANK_source', 'data_source_x', 'relations', 'data_source_y'],axis=1)
    
    print(df_WEBsal)
    print(df_WEBfreq)
    
    df_WEBfreq = df_WEBfreq.reset_index(drop=True)
    #df_WEB.index = df_WEB.index + 1   
    #df_vto.index = df_vto.index + 1 
    no_path = os.path.basename(WEBsal_file)
    filename = os.path.splitext(no_path)
    (f, ext) = filename
    
   
    #produce table with common items - this bit is working
    df_WEB_freqsal_match = pd.merge(df_WEBsal, df_WEBfreq, on=['source', 'target'], how='inner')
    df_WEB_freqsal_match = df_WEB_freqsal_match.drop_duplicates()
    
    #add the column
    df_WEB_freqsal_match['compare'] = 'both'
    print(df_WEB_freqsal_match)
    df_WEB_freqsal_match.to_csv(output_path+'freqsalmatch_'+f+'.csv', index=False)
    
    
    #merge dataframes to get common and not common
    WEBsal_all_WEBfreq_common = df_WEBsal.merge(df_WEBfreq.drop_duplicates(), on=['source', 'target'], how='left', indicator=True)
    print(WEBsal_all_WEBfreq_common)
    WEBsal_all_WEBfreq_common.to_csv(output_path+'salall_freqmatch_'+f+'.csv', index=False)
    
    WEBfreq_all_WEBsal_common = df_WEBsal.merge(df_WEBfreq.drop_duplicates(), on=['source', 'target'], how='right', indicator=True)
    print(WEBfreq_all_WEBsal_common)
    WEBfreq_all_WEBsal_common.to_csv(output_path+'freqall_salmatch'+f+'.csv', index=False)
    
    print(WEBsal_all_WEBfreq_common)
    print(WEBfreq_all_WEBsal_common)
    #vto_and_WEB 
    
    #vto_all_WEB_common['_merge'] == 'left_only'
    WEBsal_only = df_WEBsal[WEBsal_all_WEBfreq_common._merge == 'left_only']
    #WEBsal_only = WEBsal_only.drop(columns=['data_source_y', '_merge'], axis=1)
    #'relations_y',
    #vto_only = vto_only.drop('left_only')
    WEBsal_only.to_csv(output_path+'WEBsal_only_'+f+'.csv', index=False)
    #print(vto_and_WEB)

    WEBfreq_only = df_WEBfreq[WEBfreq_all_WEBsal_common._merge == 'right_only']
    #WEBfreq_only = WEBfreq_only.drop(columns=['data_source_x', '_merge'], axis=1)
    #'WEB_only = WEB_only.drop('right_only')
    #relations_x',
    WEBfreq_only.to_csv(output_path+'WEBfreq_only_'+f+'.csv', index=False)

  
    #% of common or otherwise 
    df_WEBsal_ind = float(len(df_WEBsal.index))
    print(df_WEBsal_ind)
    df_WEBfreq_ind = float(len(df_WEBfreq.index))
    print(df_WEBfreq_ind)
    WEBsal_only_ind = float(len(WEBsal_only.index))
    WEBfreq_only_ind = float(len(WEBfreq_only.index))
    in_both_ind = float(len(df_WEB_freqsal_match.index))
    #% just in WEB sal
    pcent_WEBsal = (WEBsal_only_ind/df_WEBsal_ind)*100
      
    #%common
    pcent_both_WEBsal = (in_both_ind/df_WEBsal_ind)*100
    pcent_both_WEBfreq = (in_both_ind/df_WEBfreq_ind)*100
    #% just in WEB
    pcent_WEBfreq = (WEBfreq_only_ind/df_WEBfreq_ind)*100
    
    
    #make list of items in order
    list = []
    multiple_appends(list,WEBsal_file, df_WEBsal_ind, df_WEBfreq_ind, WEBsal_only_ind, WEBfreq_only_ind, in_both_ind, pcent_WEBsal, pcent_WEBfreq, pcent_both_WEBsal, pcent_both_WEBfreq)

    print(len(list))
    return list

#     with open(output_path+'comparison_percentages_VTOsalm.txt', 'a') as file:
#         file.write(WEB_file+' in comparison with'+ vto_file + '\n')
#         
#         file.write('VTO total :' +(str(df_vto_ind))+'\n')
#         file.write('WEB total : '+ (str(df_WEB_ind))+'\n')
#         file.write('VTO not in WEB: '+ (str(vto_only_ind))+'\n')
#         file.write('WEB not in VTO: ' + (str(WEB_only_ind))+'\n')
#         file.write('VTO in WEB: ' + (str(in_both_ind))+'\n')
#          
#         file.write('Percentage only in VTO: ' + str(pcent_vto) +'\n')
#         file.write('Percentage only in WEB: ' + str(pcent_WEB) +'\n')
#         file.write('Percentage common compared to VTO: ' + str(pcent_both_vto) +'\n')
#         file.write('Percentage common compared to WEB: ' + str(pcent_both_WEB) +'\n\n')   
#                     
def main():
    input_path = './WEB_freqsalcomp/'
    output_path = './WEB_freqsalcomp/output/'
    
    filelist = os.listdir(input_path)
    i = 1
    df = pd.DataFrame()
#WEBsal_file, df_WEBsal_ind, df_WEBfreq_ind, WEBsal_only_ind, WEBfreq_only_ind, in_both_ind, pcent_WEBsal, pcent_WEBfreq, pcent_both_WEBsal, pcent_both_WEBfreq)
  
    # read in files as dataframe and change to lists
    for WEBsal_file in filelist:
        if WEBsal_file.endswith('csv'):         
            list = compare('vto_comp_WEB_SCI_freqsal_191209_rel_over5.csv', input_path, WEBsal_file, output_path)
            #printing to a file with the percentages
            df = df.append(pd.DataFrame([list], columns=('filter', 'WEBfreqsal_total', 'WEBrel5_total', 'WEBfreqsal_not_in_WEB_freq', 'WEBfreq_not_in_WEB_freqsal', 'WEBfreq_in_WEBfreqsal', '%_only_in_WEBfreqsal', '%_only_in_WEBfreq', '%_common_vs_WEBfreqsal','%_common_WEBfreq')))
    
    df.to_csv(output_path + 'comparison_percentages_WEB5vssal.csv', index=False)
    
if __name__ == "__main__":
    main()