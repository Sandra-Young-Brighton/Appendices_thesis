import os
import json

def import_names(path, filelist):
    """Loads json file and turns into a list
    """
    sci = []
    for file in filelist:
        with open(path+file, 'r') as gnrd_file:
            gnrd_names = json.load(gnrd_file)
        
            for name in gnrd_names['names']:
                sci.append(name['scientificName'])
    list_nodup = list(set(sci))
    names = open('names_list_zenodo_full.txt', 'w')

    for item in list_nodup:
        names.write(item+'\n')
  
    genup = []
    genera = []
    species = []
    subspecies = []
    for name in list_nodup:
        row = name.split(' ')
        if len(row) == 1:
            genup.append(row[0])
        if len(row) == 2:
            genera.append(row[0])
            species.append(row[1])
        if len(row) == 3:
            genera.append(row[0])
            species.append(row[1])
            subspecies.append(row[2])
        else:
            continue
    print(genup)
    print(genera)
    print(species)
    print(subspecies)
    return genera

def main():
    path = './zenodo/'
    filelist = os.listdir(path)
    import_names(path, filelist)

if __name__ == "__main__":
    main()
