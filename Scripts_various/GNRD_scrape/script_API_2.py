import requests
import os
import time
import json

def main():
    gnrd = 'https://gnrd.globalnames.org/name_finder.json'
    path = './input/'
    filelist = os.listdir(path)
	
    for file in filelist:
        gnrd = 'https://gnrd.globalnames.org/name_finder.json'
        files = {'file': (path+file, open(path+file, 'rb'), 'application/pdf')}
        r = requests.post(gnrd, {'unique': 'true', 'verbatim': 'false'}, files=files)
        gnrd_results = r.json()
        gnrd_data = json.dumps(gnrd_results)
        print(gnrd_data)
        file_next = os.path.splitext(file)
        (f,ext) = file_next
        filename = f+'GNRD.json'
        with open(filename, "w") as f:
               f.write(gnrd_data)

            

if __name__ == "__main__":
    main()

