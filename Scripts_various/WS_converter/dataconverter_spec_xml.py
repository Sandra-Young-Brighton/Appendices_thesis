"""File to select WS to convert based on one WS and one iteration (the original WS
 and then all the WS of the colloc in that WS
"""
"""
Sandra Young (February 2019)
"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET

def xml_chooser(path):
    #filelist = os.listdir(path)
    start_file = 'Salmo.xml'
    #list to parse in later step
    files_to_read = []
   
    #parse file
    tree = ET.parse(path+start_file)
    root = tree.getroot()
    #identify children of wordsketch
    children = root.findall('./wordsketch/')
    keyword = children[0]
    gramrels = children[1:]
   
    for gramrel in gramrels:
        #files_to_read = [coll.text for coll in gramrel]
        for coll in gramrel:
            files_to_read.append(coll.text)
    print(files_to_read)
    
    input_files = []

    for file in files_to_read:
        filename = file+'.xml'
        try:
            #parse file
            tree = ET.parse(path+filename)
            root = tree.getroot()
            #identify children of wordsketch
            children = root.findall('./wordsketch/')
            keyword = children[0]
            gramrels = children[1:]
           
            for gramrel in gramrels:
                #files_to_read = [coll.text for coll in gramrel]
                for coll in gramrel:
                    input_files.append(coll.text)
        except:
            print('Error: No file '+filename)
    input_files.append('Salmo')
    input_files = input_files + files_to_read
    input_files = list(set(input_files))
    print(input_files)

    return input_files
    
def xml_reader(path, input_files):
    path = './ws_nospace/'
    #read directory of wordsketches
    #filelist = os.listdir(path)
    #create overall list for DataFrame
    total_list = []
    #iterate over files
    for file in input_files:
        filename = file+'.xml'
        try:
            tree = ET.parse(path+filename)
            root = tree.getroot()
            #identify children of wordsketch
            children = root.findall('./wordsketch/')
            #identify and keep all the gramrels that I need (get the list)
            keyword = children[0]
            gramrels = children[1:]
            #print(keyword)
            #print(gramrels)
            #print(keyword.tag, keyword.attrib)
            for gramrel in gramrels:
                print(gramrel.tag, gramrel.attrib)
                for coll in gramrel:
                    print(coll.tag, coll.attrib, coll.text)
                    #set variables for coll text
                    coll_text = coll.text
                    coll_hits = coll.attrib['hits']
                    coll_score = coll.attrib['score']
                    #for each coll make a list made up of keyword, gramrel, coll hits, coll score, coll,text
                    collocates = []
                    collocates.append(keyword.text)
                    collocates.append(gramrel.attrib['name'])
                    collocates.append(coll.text)
                    collocates.append(coll_hits)
                    collocates.append(coll_score)
                    collocates.append('child-parent')
                    #print(collocates)
                    #add current list as tuple to overall collocates
                    total_list.append(tuple(collocates))
                    headers = [keyword.tag, gramrel.tag, coll.tag, 'hits', 'score', 'relations']
        except:
            continue
        print(total_list)
        
    #parse into a DataFrame
    relations = pd.DataFrame.from_records(total_list, columns=headers)
    print(relations)        
    return relations

def df_alt(relations):
    #remove unwanted gramrels (keep wanted ones) and create new one
    df_convert = relations.loc[relations['gramrel'].isin(['"X" is part of...', 'modifiers of X', 'nouns modified by X', 'X has part...', 'X is a ...', 'X is a type of...', 'X is the generic of...', "X's ..."])]
       #'X %(3.lemma) .../... %(3.lemma) X', 'X and/or ...', (add later - sibling) 
    #add parent-child column
    #df_convert = df_convert.insert(2, column='relations', value='parent-child')
    print(df_convert)      
    #set rules for parent-child column

    df_convert.loc[df_convert.gramrel == 'nouns modified by X', 'relations'] = 'parent-child'
    df_convert.loc[df_convert.gramrel == 'X has part...', 'relations'] = 'parent-child'
    df_convert.loc[df_convert.gramrel == 'X is the generic of...', 'relations'] = 'parent-child'


   
    #sibling = 'sibling' #deal with later
    
    print(df_convert)
    return df_convert
    
def convert_WS_tab(path, input_files):
    #read in Dataframe frm xml converter
    mixed_relations = xml_reader(path, input_files)
    
    #add necessary columns and remove useless gramrels
    mixed_relations = df_alt(mixed_relations)
    
    #manipulate table to have the correct headings and columns (parent-child, child-parent column)
         
    #split data into two tables - parent/child and child/parent
    parent_child_rel = mixed_relations[mixed_relations['relations']=='parent-child']
    child_parent_rel = mixed_relations[mixed_relations['relations']=='child-parent']
    
    #change both parent/child frame by removing Relation column 
    parent_child_rel = parent_child_rel.drop(['relations'], axis=1)
    child_parent_rel = child_parent_rel.drop(['relations'], axis=1)

    #rename keyword and colloc with parent and child
    parent_child_rel = parent_child_rel.rename(index=str, columns={'keyword': 'parent', 'coll': 'child'})
    print(parent_child_rel)
    
    #child/parent dataframe rename child and parent
    child_parent_rel = child_parent_rel.rename(index=str, columns={'keyword': 'child', 'coll': 'parent'})
    print(child_parent_rel)
    
    #remove WS relations column
    child_parent_rel = child_parent_rel.drop(['gramrel'], axis=1)
    print(child_parent_rel)
        
    parent_child_rel = parent_child_rel.drop(['gramrel'], axis=1)
    print(parent_child_rel)
    
    #change order of columns to be parent, child, hits, score
    reorder_cp = child_parent_rel.reindex(['parent', 'child', 'hits', 'score'], axis=1)
    
    print(reorder_cp)
    
    #concatenate both dataframes
    frames = [parent_child_rel, reorder_cp]
    all_PC_rel = pd.DataFrame().append(frames, ignore_index=True)
    all_PC_rel = all_PC_rel.reindex()
      
    return all_PC_rel
    
def sort_table(path, input_files, start_file):
    
    #convert the WS table
    all_PC_rel = convert_WS_tab(path, input_files)
    
    #split analysis type from path
    #anal = path.split(os.path.sep)
    #anal = str(anal[1])

        
    #put all upper case
    all_PC_rel = all_PC_rel.apply(lambda x:x.astype(str).str.upper())

    #change datatype to float for nnmbers
    all_PC_rel['hits'] = all_PC_rel['hits'].astype('float') 
    all_PC_rel['score'] = all_PC_rel['score'].astype('float')
        
    #drop duplicates
    all_PC_rel = all_PC_rel.drop_duplicates()
        
    #group and provide totals and means for hits and score
    aggregated = all_PC_rel.groupby(['parent', 'child'], as_index=False).aggregate({'hits': np.sum, 'score': [np.mean, np.median]})
                                                                        
    #again look at how to do the file names as they will need to change automaticall
    with open(path + '/aggregated_rel_'+start_file+'_nodup.csv', 'w') as outfile: 
        aggregated.to_csv(outfile, index=False)
            
    print(aggregated)
    
    #printing to a file the maximum hits etc to evaluate the weighting.Same issue with filename    
    totals_file = open(path + '/aggregated_rel_'+start_file+'_nodup.txt', 'w')
        
    #here do all the calculations and make variables then somehow loop to do the writing on the files
    hits_max = aggregated['hits'].max()
    print('Hits max: ' + str(hits_max))
    totals_file.write('Hits max: ' + str(hits_max) + '\n')
        
    hits_min = aggregated['hits'].min()
    print('Hits min: ' + str(hits_min))
    totals_file.write('Hits min: ' + str(hits_min) + '\n')
        
    score_mean_max = aggregated['score'].max()
    print('Score max: ' + str(score_mean_max))
    totals_file.write('Score max: ' + str(score_mean_max) + '\n')
        
    score_mean_min = aggregated['score'].min()
    print('Score min: ' + str(score_mean_min))
    totals_file.write('Score min: ' + str(score_mean_min) + '\n')
      
    return aggregated
    

def salience_weighting(path, start_file):
    """Do weighting of different types and then remove the numbers, 
    to create files for the graphs
    """
    
    #split analysis type from path
    #anal = path.split(os.path.sep)
    #anal = str(anal[1])

        
    #do bit that imports the dataframe or put it into the same file
    aggregated = pd.read_csv(os.path.join(path, 'aggregated_rel_'+start_file+'_nodup.csv'))
    
    #change datatype to float for numbers
    aggregated['Hits'] = aggregated.iloc[1:, 2].astype('float') 
    aggregated['Score'] = aggregated.iloc[1:, 3].astype('float')
        
    #do the remove rows for those outside the catchment (hits)
    i = 0
    #sort out file naming here too
    while i <= aggregated['Score'].max():
        aggregated = aggregated[aggregated['Score'] >= i]
        filename = start_file+'_sal_over'+str(i)+'.csv'
        aggregated.to_csv(os.path.join(path, 'weighted/weighted_out/salience', filename), index=False)
        i += 0.5

def weighting(path, start_file):
    """Do weighting of different types and then remove the numbers, 
    to create files for the graphs
    """
    
    #split analysis type from path
    anal = path.split(os.path.sep)
    anal = str(anal[1])

        
    #do bit that imports the dataframe or put it into the same file
    aggregated = pd.read_csv(path + '/aggregated_rel_'+start_file+'_nodup.csv')
    
    #change datatype to float for numbers
    aggregated['hits'] = aggregated.iloc[1:, 2].astype('float') 
    aggregated['score'] = aggregated.iloc[1:, 3].astype('float')
        
    #do the remove rows for those outside the catchment (hits)
    i = 0
    #sort out file naming here too
    while i <= 100:
        aggregated = aggregated[aggregated['hits'] >= i]
        aggregated.to_csv(path + 'weighted/weighted_out/'+start_file+'_rel_over'+str(i)+'.csv', index=False)
        i += 5

def main():
    path = './ws_nospace/'
    start_file = 'Salmo' 
    #input_files = xml_chooser(path)
    #sort_table(path, input_files, start_file)
    salience_weighting(path, start_file)
    weighting(path, start_file)

if __name__ == '__main__':
    main ()
    