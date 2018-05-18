import wptools
import pandas as pd
import time

def getnewname (dictname):
    return_value=''
    if dictname is not None:
        for k,v in dictname.items():
            if k=='said to be the same as (P460)':
                if type(v) is list:
                    return_value='-'.join(v)
                    break
                else:
                    return_value=v
                    break


    else:
        return ''



    return return_value

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
                value[item]= '- '.join(dic[item])
            else:
                for k, v in dic[item].items():
                    value[k] = v
                    # print(k)
                    # print(v)
        return value

    else:
        return ''


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

    newname = ''

    if item != lang_target:
        for descr in page.data['languages']:
            if descr['lang'] == lang_target:
                newname = descr['title']
    else:
        pass

    result_wikidata = {}
    try:
        result_wikidata = page.data['wikidata']
    except TypeError:
        print('typeError wikidata')
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

    if newname is not None:
        drug = newname
    alias={}
    page2 = wptools.page(drug, lang=lang_target, silent=True)
    page2.get_parse()
    page2.get_wikidata()
    try:
        alias = (page2.data['aliases'])
    except KeyError:
        print('no aliases for language ' + str(lang_target))
        try:
            alias = (page.data['aliases'])
        except KeyError:
            pass

    print('searched for ' + ' ' + item)
    print(lang_target + ': ' + drug)
    print(result_infobox)
    print(result_wikidata)
    return_value = {}

    return_value['newname'] = newname
    return_value['infobox'] = result_infobox
    return_value['wikidata'] = result_wikidata
    return_value['aliases'] = alias

    return (return_value)


drug_list = pd.read_csv('/Users/joaoalmeida/Downloads/db_match.csv', sep=";")
drug_nolink = drug_list[drug_list['Nome_Match'].isnull()]
drug_nolink = drug_nolink['Med_DCIPT_Descr']
drug_nolink = drug_nolink.drop_duplicates()
drug_nolink_noplus = drug_nolink[drug_nolink.str.contains(" +") == False]

inter = {}
inter2 = {}
final = {}
dlist = ['infobox', 'wikidata', 'aliases']
counter=1
for item in drug_nolink_noplus.tail(15):
    inter = GetDrugInfo(item, 'pt', 'en')
    if inter is not None:
        inter2 = (appendDict(inter, dlist))
        inter2['ptname'] = item
        if inter['newname'] == '':
            inter2['engname']=getnewname(inter2)
        else:
            inter2['engname'] = inter['newname']
        if counter==1:
            df = pd.DataFrame(data=inter2,index=[0])
        else:
            df.append(inter2, ignore_index=True)
        counter+=1
    else:
        pass
    print(final)

df.to_csv('/Users/joaoalmeida/Downloads/result_wiki.csv')

#Chloramphenicol testar