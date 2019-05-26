import pandas as pd
import main_utils as utils

with open("includes.txt", "r") as myfile:
    includes = eval(myfile.read())
path = includes['path']

drug_list = pd.read_csv(path, sep=";")
drug_nolink = drug_list[drug_list['Nome_Match'].isnull()]
drug_nolink = drug_nolink['Med_DCIPT_Descr']
drug_nolink = drug_nolink.drop_duplicates()
drug_nolink_noplus = drug_nolink[drug_nolink.str.contains(" +") == False]
inter = {}
inter2 = {}
final = {}
dlist = ['infobox', 'wikidata', 'aliases']
counter = 1
for item in drug_nolink_noplus.tail(15):
    inter = utils.GetDrugInfo(item, 'pt', 'en')
    if inter is not None:
        inter2 = (utils.appendDict(inter, dlist))
        inter2['ptname'] = item
        if inter['newname'] == '':
            inter2['engname'] = utils.getnewname(inter2)
        else:
            inter2['engname'] = inter['newname']
        if counter == 1:
            df = pd.DataFrame(data=inter2, index=[0])
        else:
            df.append(inter2, ignore_index=True)
        counter += 1
    else:
        pass
    print(final)

df.to_csv('result_wiki.csv')

# Chloramphenicol testar
