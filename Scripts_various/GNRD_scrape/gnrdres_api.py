import requests
import os
import time
import json

def main():
    gnrd = 'http://resolver.globalnames.org/name_resolvers.json' 
    file = {'file': ('sm_list.txt', open('sm_list.txt', 'rb'), 'text/plain')} 


    r = requests.post(gnrd, {'with_vernaculars': 'true'}, files=file)
    print(r)
#     gnrd_results = r.json()
#     gnrd_data = json.dumps(gnrd_results)
#     print(gnrd_data)
#     file_next = os.path.splitext(file)
#     (f,ext) = file_next
#     filename = f+'GNRD_res.json'
#     with open(filename, "a") as f:
#         f.write(gnrd_data)
#         time.sleep(2)
#    
        
if __name__ == "__main__":
    main()
