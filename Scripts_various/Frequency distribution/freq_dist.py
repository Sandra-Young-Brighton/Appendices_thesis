import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET
from _ast import Continue


def xml_reader(path, file):
    
    #file = 'brown_trout.xml'
    try:
        tree = ET.parse(path+file)
        print(tree)
    
        
        
        root = tree.getroot()
        print(root)
        for child in root:
            print(child.tag, child.attrib)
    
        all_doc_kws = []        
    
        #identify children of concordance
        lines = root.findall('./concordance/')
        #identify different parts of the xml
        for line in lines:
            print(line.tag)
            print(line.attrib)
            print(line.attrib['refs'])
            doc_ref = line.attrib['refs']
            kw = lines[0][1].text
            
            doc_kw = []
            
            doc_kw.append(kw)
            doc_kw.append(doc_ref)
            
            all_doc_kws.append(tuple(doc_kw))
    
        print(all_doc_kws)
        
        headers = ['keyword', 'doc_ref']
            
        #parse into a DataFrame
        count = pd.DataFrame.from_records(all_doc_kws, columns=headers)
        print(count)
        
        #freq = count['doc_ref'].value_counts()
        #print(freq)
        
        
        count['doc_count'] = count.doc_ref.map(count.doc_ref.value_counts())
        
        single_count = count.drop_duplicates().reset_index(drop=True)
    	#single_count.index = single_count.index + 1
        
        print(count)
        print(single_count)
        
        #get into the query bit for the "size "attribute
        headers = root.findall('./header/')
        subquery = headers[2][0]
        tot_freq = subquery.attrib['size']
        
        single_count['doc_total'] = 593
        
        single_count['tot_freq'] = tot_freq
        print(single_count)
            
        
        #print to csv
        single_count.to_csv(kw+'freq_dist.csv')
        
        return single_count

    except:
        print(file)

def freq_dist_calc(count):
	#calculate number of docs keyword appears in
    doc_w_kw = len(count.index)
    print(doc_w_kw)
	
	#create a dataframe with number of docs in corpus (with column #doc_ref)
    data = []
    i = 0
    
    while i < 593:
        data.append('doc#'+ str(i))
        i+= 1
    #else:
    #    print('stop loop')
    kw = count['keyword'].iloc[0]
    print(kw)
        
    print(data)
    df_tot_doc = pd.DataFrame(data, columns=['doc_ref'])
	
    print(df_tot_doc)
	
	#merge the two dataframes to be able to compare which docs have and which don't have keyword
    df_freq_dist = df_tot_doc.merge(count, on='doc_ref', how='left', indicator=True)
    
    print(df_freq_dist)
    #print to csv
    df_freq_dist.to_csv(kw+'freq_dist_tot.csv')
    
    
	
def main():
    path = './JEFF_SWU_oncmy_conc/'
    filelist = os.listdir(path)
     
    for file in filelist:
        count = xml_reader(path, file)
        freq_dist_calc(count)
		
if __name__ == '__main__':
    main ()
    