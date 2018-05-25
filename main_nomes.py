import pandas as pd
import main_utils as utils

with open ("includes.txt", "r") as myfile:
    includes=eval(myfile.read())
path=includes['path']

drug_list = pd.read_csv(path, sep=";")
drug_nolink = drug_list[drug_list['Nome_Match'].isnull()]
drug_nolink = drug_nolink['Med_DCIPT_Descr']
drug_nolink = drug_nolink.drop_duplicates()
drug_nolink_noplus = drug_nolink[drug_nolink.str.contains(" +") == False]

dlist = ['aliases']
row = 1
final = {'ptname': [], 'engname': []}
#drug_nolink_noplus=['Tenofovir','Aminofilina','Difenidramina']

for item in drug_nolink_noplus:
    inter = {}
    inter2 = {}
    inter2['ptname'] = item
    inter = utils.GetDrugInfo(item, 'pt', 'en')
    if inter is not None:
        if inter['newname'] == '':
            inter2['engname'] = utils.getsame(inter2)
        else:
            inter2['engname'] = inter['newname']
    else:
        inter2['engname'] = ''
        pass
    #print(inter2)
    for k, v in inter2.items():
        if v == '':
            final[k].append('null')
        else:
            final[k].append(v)
    print(final)
    row+=1
    if row%5==0:
        df = pd.DataFrame(data=final)
        df.to_csv('result_wikinomes.csv')

df = pd.DataFrame(data=final)
df.to_csv('result_wikinomes.csv')

# 116 e 197
# há drug_name no infobox --importante (PT: Tenofovir)
