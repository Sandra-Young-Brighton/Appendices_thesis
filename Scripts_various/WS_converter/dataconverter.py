import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os

    
def convert_WS_tab(fname, path):
    #read in Dataframe frm xml converter
    mixed_relations = multi_xml_reader()
    
    #manipulate table to have the correct headings and columns (parent-child, child-parent column)
         
    #split data into two tables - parent/child and child/parent
    parent_child_rel = mixed_relations[mixed_relations['Relation']=='parent-child']
    child_parent_rel = mixed_relations[mixed_relations['Relation']=='child-parent']
    
    #change both parent/child frame by removing Relation column 
    parent_child_rel = parent_child_rel.drop(['Relation'], axis=1)
    child_parent_rel = child_parent_rel.drop(['Relation'], axis=1)

    #rename keyword and colloc with parent and child
    parent_child_rel = parent_child_rel.rename(index=str, columns={'Keyword': 'parent', 'Colloc': 'child'})
    print(parent_child_rel)
    
    #child/parent dataframe rename child and parent
    child_parent_rel = child_parent_rel.rename(index=str, columns={'Keyword': 'child', 'Colloc': 'parent'})
    print(child_parent_rel)
    
    #remove WS relations column
    child_parent_rel = child_parent_rel.drop(['WS_relation'], axis=1)
    print(child_parent_rel)
        
    parent_child_rel = parent_child_rel.drop(['WS_relation'], axis=1)
    print(parent_child_rel)
    
    #change order of columns to be parent, child, hits, score
    reorder_cp = child_parent_rel.reindex(['parent', 'child', 'Hits', 'Score'], axis=1)
    
    print(reorder_cp)
    
    #concatenate both dataframes
    frames = [parent_child_rel, reorder_cp]
    all_PC_rel = pd.DataFrame().append(frames, ignore_index=True)
    all_PC_rel = all_PC_rel.reindex()
      
    return all_PC_rel
    
def sort_table(file, path):
    
    #convert the WS table
    all_PC_rel = convert_WS_tab(file, path)
    
    #split analysis type from path
    anal = path.split(os.path.sep)
    anal = str(anal[1])

        
    #put all upper case
    all_PC_rel = all_PC_rel.apply(lambda x:x.astype(str).str.upper())

    #change datatype to float for nnmbers
    all_PC_rel['Hits'] = all_PC_rel['Hits'].astype('float') 
    all_PC_rel['Score'] = all_PC_rel['Score'].astype('float')
        
    #drop duplicates
    all_PC_rel = all_PC_rel.drop_duplicates()
        
    #group and provide totals and means for hits and score
    aggregated = all_PC_rel.groupby(['parent', 'child'], as_index=False).aggregate({'Hits': np.sum, 'Score': [np.mean, np.median]})
                                                                        
    #again look at how to do the file names as they will need to change automatically
    with open(path + '/aggregated_rel_'+anal+'_nodup.csv', 'w') as outfile: 
        aggregated.to_csv(outfile, index=False)
            
    print(aggregated)
    
    #printing to a file the maximum hits etc to evaluate the weighting.Same issue with filename    
    totals_file = open(path + '/aggregated_rel_'+anal+'_nodup.txt', 'w')
        
    #here do all the calculations and make variables then somehow loop to do the writing on the files
    hits_max = aggregated['Hits'].max()
    print('Hits max: ' + str(hits_max))
    totals_file.write('Hits max: ' + str(hits_max) + '\n')
        
    hits_min = aggregated['Hits'].min()
    print('Hits min: ' + str(hits_min))
    totals_file.write('Hits min: ' + str(hits_min) + '\n')
        
    score_mean_max = aggregated['Score'].max()
    print('Score max: ' + str(score_mean_max))
    totals_file.write('Score max: ' + str(score_mean_max) + '\n')
        
    score_mean_min = aggregated['Score'].min()
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
    aggregated['Hits'] = aggregated.iloc[1:, 2].astype('float') 
    aggregated['Score'] = aggregated.iloc[1:, 3].astype('float')
        
    #do the remove rows for those outside the catchment (hits)
    i = 0
    #sort out file naming here too
    while i <= 100:
        aggregated = aggregated[aggregated['Hits'] >= i]
        aggregated.to_csv(path + 'weighted/weighted_out/'+anal+'_rel_over'+str(i)+'.csv', index=False)
        i += 10


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
    paths = ["./compnet/"]
    for path in paths:
        files = os.listdir(path)
        for file in files:
            if file.endswith('.csv'):
                sort_table(file, path)
                weighting(path)
                panda_tree(path)

if __name__ == '__main__':
    main ()
    