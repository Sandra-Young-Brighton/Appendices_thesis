import requests
from crossref.restful import Journals, Etiquette


def main():
    headers = {"CR-Clickthrough-Client-Token": "9abec5e0-f6c7e93a-3d6514f4-9b8311ed"}
    my_etiquette = Etiquette('corvid', '0.1', 'n/a', 's.h.young@brighton.ac.uk')  # edit this to be your details
    journals = Journals(etiquette=my_etiquette)
    jeff = journals.query("Ecology of Freshwater Fish")
    issns = {issn for journal in jeff for issn in journal["ISSN"]}
    for issn in issns:
        for article in journals.works(issn).filter(has_full_text='true'):
            res = requests.get(article["link"][0]["URL"], headers=headers)
            i = 1
            filename = "%d_out.txt" % i
            with open(filename, "w") as f:
                f.write(res.content)
                i+=1


if __name__ == "__main__":
    main()
