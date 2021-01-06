import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET


def xml_reader():
    path = './TI/'
    #read directory of wordsketches
    filelist = os.listdir(path)
    #create overall list for DataFrame
    total_list = []
    #iterate over files
    for file in filelist:
        tree = ET.parse(path+file)
        
        root = tree.getroot()
        
        for child in root:
            print(child.tag, child.attrib)
        
        #identify children of wordsketch
        children = root.findall('./wordsketch/')
        #identify and keep all the gramrels that I need (get the list)
        keyword = children[0]
        gramrels = children[1:]
        print(keyword)
        print(gramrels)
        print(keyword.tag, keyword.attrib)
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
                collocates.append('consumer/resource')
                #print(collocates)
                #add current list as tuple to overall collocates
                total_list.append(tuple(collocates))
                headers = [keyword.tag, gramrel.tag, coll.tag, 'hits', 'score', 'relations']
        #print(total_list)
        #print (headers)
        
        #parse into a DataFrame
        relations = pd.DataFrame.from_records(total_list, columns=headers)
        print(relations)
        return relations

def df_alt(relations):
    #remove unwanted gramrels (keep wanted ones) and create new one
    df_convert = relations.loc[relations['gramrel'].isin(['subjects of X', 'objects of X'])]
       #'X %(3.lemma) .../... %(3.lemma) X', 'X and/or ...', (add later - sibling) 
    #add parent-child column
    #df_convert = df_convert.insert(2, column='relations', value='parent-child')
    print(df_convert)      
    #set rules for parent-child column

    df_convert.loc[df_convert.gramrel == 'subjects of X', 'relations'] = 'consumer'
    df_convert.loc[df_convert.gramrel == 'objects of X', 'relations'] = 'resource'

    
    #sibling = 'sibling' #deal with later
    
    print(df_convert)
    return df_convert
    
def convert_WS_tab(path):
    #read in Dataframe frm xml converter
    mixed_relations = xml_reader()
     
    #add necessary columns and remove useless gramrels
    mixed_relations = df_alt(mixed_relations)
          
    #rename keyword and colloc with source and target
    mixed_relations = mixed_relations.rename(index=str, columns={'keyword': 'target', 'coll': 'source'})
    print(mixed_relations)
     
    #return mixed_relations
    #again look at how to do the file names as they will need to change automaticall
    with open(path + '/interactions_nodup.csv', 'w') as outfile: 
        mixed_relations.to_csv(outfile, index=False)
              
# def sort_table(path):
#       
#     #convert the WS table
#     all_PC_rel = convert_WS_tab()
#       
#     #split analysis type from path
#     #anal = path.split(os.path.sep)
#     #anal = str(anal[1])
#   
#           
#     #put all upper case
#     all_PC_rel = all_PC_rel.apply(lambda x:x.astype(str).str.upper())
#   
#     #change datatype to float for nnmbers
#     all_PC_rel['hits'] = all_PC_rel['hits'].astype('float') 
#     all_PC_rel['score'] = all_PC_rel['score'].astype('float')
#           
#     #drop duplicates
#     all_PC_rel = all_PC_rel.drop_duplicates()
#           
#     #group and provide totals and means for hits and score
#     aggregated = all_PC_rel.groupby(['target', 'source'], as_index=False).aggregate({'hits': np.sum, 'score': [np.mean, np.median]})
#                                                                           
#     #again look at how to do the file names as they will need to change automaticall
#     with open(path + '/interactions_nodup.csv', 'w') as outfile: 
#         aggregated.to_csv(outfile, index=False)
#               
#     print(aggregated)
#       
#     #printing to a file the maximum hits etc to evaluate the weighting.Same issue with filename    
#     totals_file = open(path + '/interactions_nodup.txt', 'w')
#           
#     #here do all the calculations and make variables then somehow loop to do the writing on the files
#     hits_max = aggregated['hits'].max()
#     print('Hits max: ' + str(hits_max))
#     totals_file.write('Hits max: ' + str(hits_max) + '\n')
#           
#     hits_min = aggregated['hits'].min()
#     print('Hits min: ' + str(hits_min))
#     totals_file.write('Hits min: ' + str(hits_min) + '\n')
#           
#     score_mean_max = aggregated['score'].max()
#     print('Score max: ' + str(score_mean_max))
#     totals_file.write('Score max: ' + str(score_mean_max) + '\n')
#          
#     score_mean_min = aggregated['score'].min()
#     print('Score min: ' + str(score_mean_min))
#     totals_file.write('Score min: ' + str(score_mean_min) + '\n')
#        
#     return aggregated
#      
#  
# def weighting(path):
#     """Do weighting of different types and then remove the numbers, 
#     to create files for the graphs
#     """
#       
#     #split analysis type from path
#     anal = path.split(os.path.sep)
#     anal = str(anal[1])
#   
#           
#     #do bit that imports the dataframe or put it into the same file
#     aggregated = pd.read_csv(path + '/interactions_nodup.csv')
#       
#     #change datatype to float for numbers
#     aggregated['hits'] = aggregated.iloc[1:, 2].astype('float') 
#     aggregated['score'] = aggregated.iloc[1:, 3].astype('float')
#           
#     #do the remove rows for those outside the catchment (hits)
#     i = 0
#     #sort out file naming here too
#     while i <= 100:
#         aggregated = aggregated[aggregated['hits'] >= i]
#         aggregated.to_csv(path + 'weighted/interactions_over'+str(i)+'.csv', index=False)
#         i += 10
#   
# 
# def panda_tree(path):
#     #create graph  
#     path = path+'weighted/weighted_out/'
#     filelist = os.listdir(path)
#     i = 1
#     # read in files as dataframe and change to lists
#     for file in filelist:
#         if file.endswith('csv'):
#             parent_child_rel = pd.read_csv(path+file)
#             parents = parent_child_rel['parent']
#             children = parent_child_rel['child']
# 
#             # change lists to tuples
#             relations = pd.DataFrame({'from': parents, 'to': children})
#             print(relations)
#  
#             # Build your graph
#             graph_name = 'G%s' %i
#             graph_name=nx.from_pandas_edgelist(relations, 'from', 'to', create_using=nx.DiGraph())
#  
#             # Plot it
#             nx.draw(graph_name, with_labels=True)
#             no_path = os.path.basename(file)
#             filename = os.path.splitext(no_path)
#             (f, ext) = filename
#             plt.savefig(path+'directed/'+f+'_dirgraph.png')
#             plt.clf()
#             i+=1
            
def main():
    path = './TI/' 
    #sort_table(path)
    convert_WS_tab(path)
    #panda_tree(path)

if __name__ == '__main__':
    main ()
    