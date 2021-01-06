import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET


def xml_reader(file):
    #create overall list for DataFrame
    total_list = []
    #iterate over files
    
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
            collocates.append('child-parent')
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
    df_convert = relations.loc[relations['gramrel'].isin(['subjects of X', 'objects of X', '“X" is part of...', 'modifiers of X', 'nouns modified by X', 'X has part...', 'X is a ...', 'X is a type of...', 'X is the generic of...', "X's ..."])].copy()
       #'X %(3.lemma) .../... %(3.lemma) X', 'X and/or ...', (add later - sibling) 
    #add parent-child column
    #df_convert = df_convert.insert(2, column='relations', value='parent-child')
    print(df_convert)      
    #set rules for parent-child column

    df_convert.loc[df_convert.gramrel == 'nouns modified by X', 'relations'] = 'parent-child'
    df_convert.loc[df_convert.gramrel == 'X has part...', 'relations'] = 'parent-child'
    df_convert.loc[df_convert.gramrel == 'X is the generic of...', 'relations'] = 'parent-child'
    df_convert.loc[df_convert.gramrel == 'subjects of X', 'relations'] = 'eats' #colloc is consumer
    df_convert.loc[df_convert.gramrel == 'objects of X', 'relations'] = 'is eaten by' #colloc is resource


   
    #sibling = 'sibling' #deal with later
    
    print(df_convert)
    return df_convert
    
def convert_WS_tab():
    #read in Dataframe from xml converter
    mixed_relations = xml_reader()
    
    #add necessary columns and remove useless gramrels
    mixed_relations = df_alt(mixed_relations)
    
    #manipulate table to have the correct headings and columns (parent-child, child-parent column)
         
    #split data into two tables - parent/child and child/parent
    parent_child_rel = mixed_relations[mixed_relations['relations']=='parent-child']
    child_parent_rel = mixed_relations[mixed_relations['relations']=='child-parent']
    consumer_resource = mixed_relations[mixed_relations['relations']=='eats']
    resource_consumer = mixed_relations[mixed_relations['relations']=='is eaten by']
    
     #change both parent/child frame by removing Relation column 
#     parent_child_rel = parent_child_rel.drop(['relations'], axis=1)
#     child_parent_rel = child_parent_rel.drop(['relations'], axis=1)

    #rename keyword and colloc with parent and child
    parent_child_rel = parent_child_rel.rename(index=str, columns={'keyword': 'source', 'coll': 'target'})
    print(parent_child_rel)
    
    #child/parent dataframe rename child and parent
    child_parent_rel = child_parent_rel.rename(index=str, columns={'keyword': 'target', 'coll': 'source'})
    print(child_parent_rel)
    
    #consumer_resource dataframe rename source target
    consumer_resource = consumer_resource.rename(index=str, columns={'keyword': 'target', 'coll': 'source'})
    print(consumer_resource)
    
    #consumer_resource dataframe rename source target
    resource_consumer = resource_consumer.rename(index=str, columns={'keyword': 'target', 'coll': 'source'})
    print(resource_consumer)
    
    #remove WS relations column
    child_parent_rel = child_parent_rel.drop(['gramrel'], axis=1)
    print(child_parent_rel)
        
    parent_child_rel = parent_child_rel.drop(['gramrel'], axis=1)
    print(parent_child_rel)
    
    consumer_resource = consumer_resource.drop(['gramrel'], axis=1)
    print(consumer_resource)
    
    resource_consumer = resource_consumer.drop(['gramrel'], axis=1)
    print(resource_consumer)
    
    #change order of columns to be parent, child, hits, score
    reorder_cp = child_parent_rel.reindex(['source', 'target', 'hits', 'score'], axis=1)
    print(reorder_cp)
    
    reorder_cr = consumer_resource.reindex(['source', 'target', 'hits', 'score'], axis=1)
    print(reorder_cr)
    
    reorder_rc = resource_consumer.reindex(['source', 'target', 'hits', 'score'], axis=1)
    print(reorder_rc)
    
    #concatenate both dataframes
    frames = [parent_child_rel, reorder_cp, reorder_cr, reorder_rc]
    all_PC_rel = pd.DataFrame().append(frames, ignore_index=True)
    all_PC_rel = all_PC_rel.reindex()
      
    return all_PC_rel
    
def sort_table(path, filelist):
    
    #convert the WS table
    all_PC_rel = convert_WS_tab(path, filelist)
    
    #split analysis type from path
    anal = path.split(os.path.sep)
    anal = str(anal[1])

        
    #put all upper case
    all_PC_rel = all_PC_rel.apply(lambda x:x.astype(str).str.upper())

    #change datatype to float for nnmbers
    all_PC_rel['hits'] = all_PC_rel['hits'].astype('float') 
    all_PC_rel['score'] = all_PC_rel['score'].astype('float')
        
    #drop duplicates
    all_PC_rel = all_PC_rel.drop_duplicates()
        
    #group and provide totals and means for hits and score
    aggregated = all_PC_rel.groupby(['source', 'target'], as_index=False).aggregate({'hits': np.sum, 'score': [np.mean, np.median]})
                                                                        
    #again look at how to do the file names as they will need to change automaticall
    with open(path + '/aggregated_rel_'+anal+'_nodup.csv', 'w') as outfile: 
        aggregated.to_csv(outfile, index=False)
            
    print(aggregated)
    
    #printing to a file the maximum hits etc to evaluate the weighting.Same issue with filename    
    totals_file = open(path + '/aggregated_rel_'+anal+'_nodup.txt', 'w')
        
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
    

def weighting(path):
    """Do weighting of different types and then remove the numbers, 
    to create files for the graphs
    """
    
    #split analysis type from path
    anal = path.split(os.path.sep)
    anal = str(anal[1])

        
    #do bit that imports the dataframe or put it into the same file
    aggregated = pd.read_csv(path + '/aggregated_rel_'+anal+'_nodup.csv')
    
    #change datatype to float for numbers
    aggregated['hits'] = aggregated.iloc[1:, 3].astype('float') 
    aggregated['score'] = aggregated.iloc[1:, 4].astype('float')
        
    #do the remove rows for those outside the catchment (hits)
    i = 0
    #sort out file naming here too
    while i <= 100:
        aggregated = aggregated[aggregated['hits'] >= i]
        aggregated.to_csv(path + 'weighted/weighted_out/'+anal+'_rel_over'+str(i)+'.csv', index=False)
        i += 5

def salience_weighting(path):
    """Do weighting of different types and then remove the numbers, 
    to create files for the graphs
    """
    
    #split analysis type from path
    anal = path.split(os.path.sep)
    anal = str(anal[1])

        
    #do bit that imports the dataframe or put it into the same file
    aggregated = pd.read_csv(os.path.join(path, 'aggregated_rel_'+anal+'_nodup.csv'))
    
    #change datatype to float for numbers
    aggregated['Hits'] = aggregated.iloc[1:, 2].astype('float') 
    aggregated['Score'] = aggregated.iloc[1:, 3].astype('float')
        
    #do the remove rows for those outside the catchment (hits)
    i = 0
    #sort out file naming here too
    while i <= aggregated['Score'].max():
        aggregated = aggregated[aggregated['Score'] >= i]
        filename = anal+'_sal_over'+str(i)+'.csv'
        aggregated.to_csv(os.path.join(path, 'weighted/weighted_out/salience', filename), index=False)
        i += 0.5
        
def panda_tree(path):
    #create graph  
    path = path+'weighted/weighted_out/'
    filelist = os.listdir(path)
    i = 1
    # read in files as dataframe and change to lists
    for file in filelist:
        if file.endswith('csv'):
            parent_child_rel = pd.read_csv(path+file)
            parents = parent_child_rel['parent']
            children = parent_child_rel['child']

            # change lists to tuples
            relations = pd.DataFrame({'from': parents, 'to': children})
            print(relations)
 
            # Build your graph
            graph_name = 'G%s' %i
            graph_name=nx.from_pandas_edgelist(relations, 'from', 'to', create_using=nx.DiGraph())
 
            # Plot it
            nx.draw(graph_name, with_labels=True)
            no_path = os.path.basename(file)
            filename = os.path.splitext(no_path)
            (f, ext) = filename
            plt.savefig(path+'directed/'+f+'_dirgraph.png')
            plt.clf()
            i+=1
            
def main():
    path = './zenodo/' 
	    path = './zenodo/'
    #read directory of wordsketches
    filelist = os.listdir(path)
	for file in filelist:
		sort_table(path, filelist)
		weighting(path)
		salience_weighting(path)
    #panda_tree(path)

if __name__ == '__main__':
    main ()
    