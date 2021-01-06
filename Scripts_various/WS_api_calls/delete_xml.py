import os
import xml.etree.ElementTree as ET

def delete_xml(path, filelist):
        
    for file in filelist:
        if file.endswith('.xml'):
                os.remove(path+file)
        else:
            continue
        
def main():
    path = './' 
    filelist = os.listdir(path)
    delete_xml(path, filelist)

if __name__ == '__main__':
    main ()
    