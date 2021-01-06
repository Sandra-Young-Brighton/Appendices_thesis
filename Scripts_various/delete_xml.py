import os
import xml.etree.ElementTree as ET

def delete_xml(path, filelist):
#     for file in filelist:
#         if file.endswith('.py'):
#             print(file)
#             os.remove(path+file)
#         else:
#             continue
        
    for file in filelist:
        if file.endswith('.xml'):
            if 'HTTP 429' in open(path+file).read():
                print(file)
                os.remove(path+file)
            elif 'http://www.w3.org/1999/xhtml' in open(path+file).read():
                print(file)
                os.remove(path+file)
            else:
                continue
        
def main():
    path = './zenodo/' 
    filelist = os.listdir(path)
    delete_xml(path, filelist)

if __name__ == '__main__':
    main ()
    