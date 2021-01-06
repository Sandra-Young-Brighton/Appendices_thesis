import requests
from crossref.restful import Journals, Etiquette, Works
import time


def main():
    headers = {"CR-Clickthrough-Client-Token": "9abec5e0-f6c7e93a-3d6514f4-9b8311ed", 'X-Rate-Limit-Interval': "1", 'X-Rate-Limit-Limit': "50"}
    my_etiquette = Etiquette('melopomene', '0.1', 'n/a', 's.h.young@brighton.ac.uk')  # edit this to be your details
    works = Works(etiquette=my_etiquette)
    journals = Journals(etiquette=my_etiquette)
    #s = 1
    urls = []
    query = works.query("gracilaria").filter(has_full_text='true',).count()
    print(query)
    query = works.query("gracilaria").filter(has_full_text='true',)
    for item in query:
        print(item)
        title = str(item['title'])
        res = requests.get(item["link"][0]["URL"], headers=headers)
        path = './gracilaria/'
        filename = title+".pdf"
        with open(filename, "w") as f:
            f.write(res.content)
            #s+=1
        time.sleep(5)

    
#     for issn in issns:
#         for article in journals.works(issn).filter(has_full_text='true',):
#             res = requests.get(article["link"][0]["URL"], headers=headers)
#             filename = "./out/%d.pdf" % i
#             with open(filename, "w") as f:
#                 f.write(res.content)
#                 i+=1
# 
#             time.sleep(2)

if __name__ == "__main__":
    main()
