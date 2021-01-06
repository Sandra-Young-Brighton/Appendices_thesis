#select all VTO entries relating to Salmonidae (higher and lower ranks)

import os
import pandas as pd

def vto_rank_search(vto_file):
	#read in VTO dataframe with source and target sorted
	df_vto = pd.read_csv(vto_file)
	#print(df_vto)
	
	#remove dangling whitespace
	df_vto = df_vto.apply(lambda x: x.str.strip())
	#print(df_vto)
	#df_vto.to_csv('vto_test_output.csv')
	
	#select the Poeciliidae target and source examples in the dataframe
	rank_fam = df_vto[df_vto.source == 'Poeciliidae']
	print('1:', rank_fam)
	print(type(rank_fam))
	rank_up = df_vto[df_vto.target == 'Poeciliidae']
	print('2:', rank_up)
	print(type(rank_up))
	
	#select higher ranks of Poeciliidae to add to the table
	rank_higher = str(rank_up['source'])
	rank_higher = rank_higher.split()[1]
	print('3:', rank_higher)
	
	#search for ancestors of upper ranks from Poeciliidae (order)
	rank_upper = df_vto[df_vto.target == rank_higher]
	print('4:', rank_upper)
	
	#salmonidae superorder
	#select higher ranks of Poeciliidae to add to the table
	rank_sorder = str(rank_upper['source'])
	rank_sorder = rank_sorder.split()[1]
	print('5:', rank_sorder)
	
	#search for ancestors of upper ranks from Salmonidae (order)
	df_rank_sorder = df_vto[df_vto.target == rank_sorder]
	print('6:', df_rank_sorder)
	
	#infraclass
		#select higher ranks of Salmonidae to add to the table
	rank_inclass = str(df_rank_sorder['source'])
	rank_inclass = rank_inclass.split()[1]
	print('7:', rank_inclass)
	
	#search for ancestors of upper ranks from Salmonidae (order)
	df_rank_inclass = df_vto[df_vto.target == rank_inclass]
	print('8:', df_rank_inclass)
	
	#search for lower ranks
	rank_lower = rank_fam['target']
	list_rank_lower = rank_lower.tolist()
	print('9:', list_rank_lower)
	rank_downrank = df_vto.loc[df_vto['source'].isin(list_rank_lower)]
	print('10:', rank_downrank)
	
	#search for species level down
	rank_species = rank_downrank['target']
	list_rank_species = rank_species.tolist()
	print('11:', rank_species)
	rank_bottom = df_vto.loc[df_vto['source'].isin(list_rank_species)]
	print('12:', rank_bottom)
	
	vto_rank = [rank_fam, rank_up, rank_upper, df_rank_sorder, df_rank_inclass, rank_downrank, rank_bottom]
	
	rank_total = pd.concat(vto_rank, axis=0, ignore_index=True)
	print(rank_total)
	
	rank_total.to_csv('VTO_poeciliidae_190918.csv', index=False)
	
def main():
      vto_rank_search('vto_taxrank_sourcetarget_190619.csv')
    
    
if __name__ == "__main__":
    main()