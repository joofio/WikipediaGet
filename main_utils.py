import wptools


def getsame(dictname):
    return_value = ''
    if dictname is not None:
        for k, v in dictname.items():
            if k == 'said to be the same as (P460)':
                if type(v) is list:
                    return_value = '-'.join(v)
                    break
                else:
                    return_value = v
                    break
    else:
        return ''

    return return_value


def getnewname(page, lang_target, infobox,wikidata):
    name = ''
    try:
        for descr in page.data['languages']:
            if descr['lang'] == lang_target:
                name = descr['title']
                break
    except KeyError:
        pass

    if name == '':
        for k, v in infobox.items():
            if k == 'drug_name':#tenofovir
                name = v
                break
    if name == '':
        for k, v in infobox.items():
            if k == 'name':#sene
                name = v
                break
    if name == '':
        list=['Commons category (P373)']
        namesfromwiki=appendDict(wikidata,list)
        name=namesfromwiki[list[0]]
    return name


def appendDict(dic, dlist):
    value = {}
    if dic is not None:
        for item in dlist:
            if type(dic[item]) is dict and len(dic[item]) > 1:
                for k, v in dic[item].items():
                    if type(v) is dict:
                        for k2, v2 in v.items():
                            value[k + '_' + k2] = v2
                    elif type(v) is list:
                        if v is not None:
                            value[k] = '- '.join(v)
                    elif type(v) is str:
                        value[k] = v
                        # print(k)
                        # print(v)
                    else:
                        pass
            elif type(dic[item]) is list:
                value[item] = '- '.join(dic[item])
            elif type(dic[item]) is dict:
                for k, v in dic[item].items():
                    value[k] = v
            else:
                value[item]=dic[item]
                    # print(k)
                    # print(v)
        return value

    else:
        return dic


def handleLang(drug, lang):
    try:
        page = wptools.page(drug, lang=lang, silent=True)
        page.get_parse()
        page.get_wikidata()
        page.get_more()
        return page
    except:
        return False


def GetDrugInfo(drug, lang_origin, lang_target):
    ''' Takes drug name and searches wikipedia
    for the details and aliases '''
    page = wptools.page(drug, lang=lang_origin, silent=True)

    list_lang = [lang_target, lang_origin, 'es']
    for item in list_lang:
        page = handleLang(drug, item)
        if page != False:
            break

    if page is False:
        return

    result_wikidata = {}
    try:
        result_wikidata = page.data['wikidata']
    except TypeError:
        print('TypeError wikidata')
        pass

    result_infobox = {}
    try:
        for i in page.data['infobox']:
            info = page.data['infobox'][i]
            info = info.replace('[[', '')
            info = info.replace(']]', '')
            info = info.replace("''", '')
            info = info.replace('<br>', '')
            info = info.replace('&nbsp;', ' ')
            result_infobox[i] = info
    except TypeError:
        print('typeError infobox')
        pass
    newname = getnewname(page, lang_target, result_infobox,result_wikidata)

    if newname is not None:
        drug = newname

    alias = {}
    page2 = wptools.page(drug, lang=lang_target, silent=True)
    page2.get_parse()
    page2.get_wikidata()
    try:
        alias = (page2.data['aliases'])
    except KeyError:
        #print('no aliases for language ' + str(lang_target))
        try:
            alias = (page.data['aliases'])
        except KeyError:
            pass

    print(drug)
    print('infobox')
    print(result_infobox)
    print('wikidata')
    print(result_wikidata)
    return_value = {}

    return_value['newname'] = newname
    return_value['infobox'] = result_infobox
    return_value['wikidata'] = result_wikidata
    return_value['aliases'] = alias

    return (return_value)
