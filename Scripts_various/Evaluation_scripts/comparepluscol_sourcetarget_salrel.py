#compare the edges lists of VTO versus the data

import pandas as pd
import os
import numpy as np

def multiple_appends(listname, *element):
    listname.extend(element)

def compare(jeffsal_file, input_path, jefffreq_file, output_path):
    #read in both dataframes
    df_jeffsal = pd.read_csv(jeffsal_file)
    df_jefffreq = pd.read_csv(input_path+jefffreq_file)
    
    print(df_jefffreq)
    print(df_jeffsal)
    
    
    #change  columns to denote the datafame
    df_jeffsal.loc[:,'data_source'] = 'JEFF salience'
    df_jefffreq.loc[:, 'data_source'] = 'JEFF frequency' 
    df_jeffsal.loc[:, '_merge'].replace('both', 'VTO match')
    df_jefffreq.loc[:, '_merge'].replace('both', 'VTO match')
    df_jeffsal.loc[:, '_merge'].replace('right_only', 'JEFF only')
    df_jefffreq.loc[:, '_merge'].replace('right_only', 'JEFF only') 
    
    df_jeffsal.rename(columns={'_merge': 'included'}, inplace=True)
    df_jefffreq.rename(columns={'_merge': 'included'}, inplace=True)
    #drop unnecessary columns
    df_jeffsal.drop(['TAXRANK_target', 'TAXRANK_source', 'data_source_x', 'relations', 'data_source_y'], axis=1)
    df_jefffreq.drop(['TAXRANK_target', 'TAXRANK_source', 'data_source_x', 'relations', 'data_source_y'],axis=1)
    
    print(df_jeffsal)
    print(df_jefffreq)
    
    df_jefffreq = df_jefffreq.reset_index(drop=True)
    #df_jeff.index = df_jeff.index + 1   
    #df_vto.index = df_vto.index + 1 
    no_path = os.path.basename(jefffreq_file)
    filename = os.path.splitext(no_path)
    (f, ext) = filename
    
   
    #produce table with common items - this bit is working
    df_jeff_freqsal_match = pd.merge(df_jeffsal, df_jefffreq, on=['source', 'target'], how='inner')
    df_jeff_freqsal_match = df_jeff_freqsal_match.drop_duplicates()
    
    #add the column
    df_jeff_freqsal_match['compare'] = 'both'
    print(df_jeff_freqsal_match)
    df_jeff_freqsal_match.to_csv(output_path+'freqsalmatch_'+f+'.csv', index=False)
    
    
    #merge dataframes to get common and not common
    jeffsal_all_jefffreq_common = df_jeffsal.merge(df_jefffreq.drop_duplicates(), on=['source', 'target'], how='left', indicator=True)
    print(jeffsal_all_jefffreq_common)
    jeffsal_all_jefffreq_common.to_csv(output_path+'jeffsal_all_jefffreq_common_'+f+'.csv', index=False)
    
    jefffreq_all_jeffsal_common = df_jeffsal.merge(df_jefffreq.drop_duplicates(), on=['source', 'target'], how='right', indicator=True)
    print(jefffreq_all_jeffsal_common)
    jefffreq_all_jeffsal_common.to_csv(output_path+'jefffreq_all_jeffsal_common_'+f+'.csv', index=False)
    
    print(jeffsal_all_jefffreq_common)
    print(jefffreq_all_jeffsal_common)
    #vto_and_jeff 
    
    #vto_all_jeff_common['_merge'] == 'left_only'
    jeffsal_only = df_jeffsal[jeffsal_all_jefffreq_common._merge == 'left_only']
    #jeffsal_only = jeffsal_only.drop(columns=['data_source_y', '_merge'], axis=1)
    #'relations_y',
    #vto_only = vto_only.drop('left_only')
    jeffsal_only.to_csv(output_path+'jeffsal_only_'+f+'.csv', index=False)
    #print(vto_and_jeff)

    jefffreq_only = df_jefffreq[jefffreq_all_jeffsal_common._merge == 'right_only']
    #jefffreq_only = jefffreq_only.drop(columns=['data_source_x', '_merge'], axis=1)
    #'jeff_only = jeff_only.drop('right_only')
    #relations_x',
    jefffreq_only.to_csv(output_path+'jeff_only_'+f+'.csv', index=False)

  
    #% of common or otherwise 
    df_jeffsal_ind = float(len(df_jeffsal.index))
    print(df_jeffsal_ind)
    df_jefffreq_ind = float(len(df_jefffreq.index))
    print(df_jefffreq_ind)
    jeffsal_only_ind = float(len(jeffsal_only.index))
    jefffreq_only_ind = float(len(jefffreq_only.index))
    in_both_ind = float(len(df_jeff_freqsal_match.index))
    #% just in JEFF sal
    pcent_jeffsal = (jeffsal_only_ind/df_jeffsal_ind)*100
      
    #%common
    pcent_both_jeffsal = (in_both_ind/df_jeffsal_ind)*100
    pcent_both_jefffreq = (in_both_ind/df_jefffreq_ind)*100
    #% just in JEFF
    pcent_jefffreq = (jefffreq_only_ind/df_jefffreq_ind)*100
    
    
    #make list of items in order
    list = []
    multiple_appends(list,jeffsal_file, df_jeffsal_ind, df_jefffreq_ind, jeffsal_only_ind, jefffreq_only_ind, in_both_ind, pcent_jeffsal, pcent_jefffreq, pcent_both_jeffsal, pcent_both_jefffreq)

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
    input_path = './191206_freqsal_test/'
    output_path = './191206_output_test/'
    
    filelist = os.listdir(input_path)
    i = 1
    df = pd.DataFrame()
    
    # read in files as dataframe and change to lists
    for jefffreq_file in filelist:
        if jefffreq_file.endswith('csv'):         
            list = compare('jeff_all_vto_common_jeff_SCI_only_salfreq191202_rel_over4_sal11.csv', input_path, jefffreq_file, output_path)
            #printing to a file with the percentages
            df = df.append(pd.DataFrame([list], columns=('filter', 'JEFFsal411_total', 'JEFFrel5_total', 'JEFFfreqsal_not_in_JEFF_freq', 'JEFFfreq_not_in_JEFF_freqsal', 'JEFFfreqsal_in_JEFFfreq', '%_only_in_JEFFfreqsal', '%_only_in_JEFFfreq', '%_common_vs_JEFFfresal','%_common_JEFFfreq')))
    
    df.to_csv(output_path + 'comparison_percentages_jeff411vs5.csv', index=False)
    
if __name__ == "__main__":
    main()