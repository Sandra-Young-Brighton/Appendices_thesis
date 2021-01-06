#select all VTO entries relating to Salmonidae (higher and lower ranks)

import os
import pandas as pd

def vto_salm(vto_file):
	#read in VTO dataframe with source and target sorted
	df_vto = pd.read_csv(vto_file)
	#print(df_vto)
	
	#remove dangling whitespace
	df_vto = df_vto.apply(lambda x: x.str.strip())
	#print(df_vto)
	#df_vto.to_csv('vto_test_output.csv')
	
	#select the Salmonidae target and source examples in the dataframe
	salmonidae_fam = df_vto[df_vto.source == 'Salmonidae']
	print('1:', salmonidae_fam)
	print(type(salmonidae_fam))
	salmonidae_up = df_vto[df_vto.target == 'Salmonidae']
	print('2:', salmonidae_up)
	print(type(salmonidae_up))
	
	#select higher ranks of Salmonidae to add to the table
	salmonidae_higher = str(salmonidae_up['source'])
	salmonidae_higher = salmonidae_higher.split()[1]
	print('3:', salmonidae_higher)
	
	#search for ancestors of upper ranks from Salmonidae (order)
	salmonidae_upper = df_vto[df_vto.target == salmonidae_higher]
	print('4:', salmonidae_upper)
	
	#salmonidae superorder
	#select higher ranks of Salmonidae to add to the table
	salmonidae_sorder = str(salmonidae_upper['source'])
	salmonidae_sorder = salmonidae_sorder.split()[1]
	print('5:', salmonidae_sorder)
	
	#search for ancestors of upper ranks from Salmonidae (order)
	df_salmonidae_sorder = df_vto[df_vto.target == salmonidae_sorder]
	print('6:', df_salmonidae_sorder)
	
	#infraclass
		#select higher ranks of Salmonidae to add to the table
	salmon_inclass = str(df_salmonidae_sorder['source'])
	salmon_inclass = salmon_inclass.split()[1]
	print('7:', salmon_inclass)
	
	#search for ancestors of upper ranks from Salmonidae (order)
	df_salmon_inclass = df_vto[df_vto.target == salmon_inclass]
	print('8:', df_salmon_inclass)
	
	#search for lower ranks
	salmonidae_lower = salmonidae_fam['target']
	list_salm_lower = salmonidae_lower.tolist()
	print('9:', list_salm_lower)
	salmonidae_downrank = df_vto.loc[df_vto['source'].isin(list_salm_lower)]
	print('10:', salmonidae_downrank)
	
	#search for species level down
	salmonidae_species = salmonidae_downrank['target']
	list_salm_species = salmonidae_species.tolist()
	print('11:', salmonidae_species)
	salmonidae_bottom = df_vto.loc[df_vto['source'].isin(list_salm_species)]
	print('12:', salmonidae_bottom)
	
	vto_salmonidae = [salmonidae_fam, salmonidae_up, salmonidae_upper, df_salmonidae_sorder, df_salmon_inclass, salmonidae_downrank, salmonidae_bottom]
	
	salmonidae_total = pd.concat(vto_salmonidae, axis=0, ignore_index=True)
	print(salmonidae_total)
	
	salmonidae_total.to_csv('VTO_salmonidae_190619.csv', index=False)
	
def main():
      vto_salm('vto_taxrank_sourcetarget_190619.csv')
    
    
if __name__ == "__main__":
    main()