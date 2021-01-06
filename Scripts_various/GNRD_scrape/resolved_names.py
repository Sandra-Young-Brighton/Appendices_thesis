import json
import os
import pprint

file = '1_out_GNRD.json'
with open(file, 'r') as gnrd_file:
    gnrd_names = json.load(gnrd_file)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(gnrd_names.keys())
    pp.pprint(gnrd_names.items())
    
    print(gnrd_names['resolved_names']['name_string'])
        