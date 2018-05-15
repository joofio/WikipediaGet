import wptools

def getDrugInfo(drug, lang):
    page = wptools.page(drug)

    page.get_parse()
    #print(page.data['infobox'])
    page.get_wikidata()
    print('wikidata-----')
    print(page.data['wikidata'])
    #print('aliases-----')
    #print(page.data['aliases'])
    #print('labels------')
    #print(page.data['labels'])

    result={}
    try:
        for i in page.data['infobox']:
            info =page.data['infobox'][i]
            info = info.replace('[[','')
            info = info.replace(']]','')
            info = info.replace("''", '')
            info = info.replace('<br>','')
            info = info.replace('&nbsp;',' ')

            result[i] = info
    except TypeError:
        pass

    page2 = wptools.page(drug,lang=lang)
    page2.get_parse()
    page2.get_wikidata()
    print(page2.data['aliases'])


    print(result.keys())
    print(result.values())

getDrugInfo('paracetamol','ar')
