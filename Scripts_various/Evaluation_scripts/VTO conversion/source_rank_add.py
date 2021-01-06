import pandas as pd
import csv

df = pd.read_csv('vto_target_taxrankname.csv')

df = df.drop(df.columns[0], axis=1)

df = df.rename(columns={'TAXRANK':'TAXRANK_target'})

#if values in target column are not duplicated
#s = df.set_index('target')['TAXRANK_target']
#if possible duplicated keep first value only
s = df.drop_duplicates('target').set_index('target')['TAXRANK_target']
df['TAXRANK_source'] = df['source'].map(s).reset_index(drop=True)
print (df)

df.to_csv('vto_taxrank_sourcetarget.csv', index=False)

# def main():
#     input_path = './input_files/'
#     output_path = './jeff_ranks_plus_source/'
#     
# #     filelist = os.listdir(input_path)
# #     i = 1
# #     # read in files as dataframe and change to lists
# #     for jeff_file in filelist:
# #         if jeff_file.endswith('csv'):         
# #             rank_add('vto_target_taxrankname.csv', input_path, jeff_file, output_path)
#     
# if __name__ == '__main__':
#     main ()