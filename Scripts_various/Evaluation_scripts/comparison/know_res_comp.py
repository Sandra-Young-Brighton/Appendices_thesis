#create tables of names which are common across datasets, those which are only in one or another 
#[ITIS, CoL and VTO]

import pandas as pd
import os
import numpy as np

def compare(file):
	#read in csv file with columns: knowledge resource, type of name, name, language, country, URL
	know_res_table = pd.read_csv()
	know_res_table = know_res_table.apply(lambda x: x.astype(str).str.strip())
	
	#accepted names
	accept_name = know_res_table.loc['Accepted name', 'Type of name']
	print(accept_name)
	
	#matching synonyms across all three datasets
	match_all_syn = know_res_table[know_res_table.duplicated(['Type of name', 'Name'])]
	print(match_all_syn)
	
	match_synonyms = match_all_syn['Synonym', 'Type of name']
	match_comm = match_all_syn['Common name', 'Type of name']
	print(match_synonyms)
	print(match_comm)
	
	#identify unique
	unique_ent = know_res_table.drop_duplicates(subset=['Type of name', 'Name'], keep=False)
	
	#synonyms only in VTO
	vto_only = unique_ent['VTO', 'Knowledge resource']
	print(vto_only)
	
	#synonyms only in CoL
	col_only = unique_ent['CoL', 'Knowledge resource']
	print(col_only)
	
	#synonyms only in ITIS
	itis_only = unique_ent['ITIS', 'Knowledge resource']
	print(itis_only)
	

def main():
    
	path = 
    file = 'know_res_comparison.csv'
    
	compare(file)
	
if __name__ == "__main__":
    main()