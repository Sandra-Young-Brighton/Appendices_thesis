"""Script to replace MWU names with the same without spaces for further analysis
"""
"""
Created on 22 Jan 2019
by Sandra
"""

import os
import json
from re import sub

def replace_linebreak(file):
    output = file.replace('\n', ' ').replace('\r', ' ').replace('  ', ' '),replace('\t', ' ')
    return output
        
def main():
    path = './jeff_in/'
    filelist = os.listdir(path)
    
    for filename in filelist:
        file = open(path+filename, 'r').read()
        path2 = './jeff_in_fixed/'
        output = replace_linebreak(file)
        filename, file_extension = os.path.splitext(filename)
        f = open(path2+filename+'_fixed.txt', 'w')                   #what file you want to write to
        f.write(output)                                       #write to the file
        #print(output)       

if __name__ == '__main__':
    main ()