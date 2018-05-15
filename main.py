import wikipediaapi
import requests, json
import wptools

# wiki_wiki = wikipediaapi.Wikipedia('en')
#
# page_py = wiki_wiki.page('paracetamol')
# print("Page - Exists: %s" % page_py.exists())
#
# print("Page - Title: %s" % page_py.title)
# # Page - Title: Python (programming language)
#
# print("Page - Summary: %s" % page_py.summary[0:60])
# # Page - Summary: Python is a widely used high-level programming language for
#
# print(page_py.fullurl)
# # https://en.wikipedia.org/wiki/Python_(programming_language)
#
# print(page_py.canonicalurl)
# # https://en.wikipedia.org/wiki/Python_(programming_language)
#
# wiki_wiki = wikipediaapi.Wikipedia(
#         language='en',
#         extract_format=wikipediaapi.ExtractFormat.WIKI
# )
#
# p_wiki = wiki_wiki.page("paracetamol")
# #print(p_wiki.text)
# # Summary
# # Section 1
# # Text of section 1
# # Section 1.1
# # Text of section 1.1
#
# wiki_html = wikipediaapi.Wikipedia(
#         language='en',
#         extract_format=wikipediaapi.ExtractFormat.HTML
# )
# p_html = wiki_html.page("paracetamol")
# #print(p_html.text)
# # <p>Summary</p>
# # <h2>Section 1</h2>
# # <p>Text of section 1</p>
# # <h3>Section 1.1</h3>
# # <p>Text of section 1.1</p>
#
# def print_sections(sections, level=0):
#     for s in sections:
#         print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
#         print_sections(s.sections, level + 1)
#
#
# print_sections(page_py.sections)

def getTaxonomy(title):
    r = requests.get('https://en.wikipedia.org/w/api.php?action=query&titles=' + title  + '&prop=revisions&rvprop=content&rvsection=0&format=json')

    a = ''
    t = json.loads(r.text)
    for i in t['query']['pages']:
        a = t['query']['pages'][ i ]['revisions'][0]['*']


    taxobox = axobox = a[a.upper().index('{{DRUGBOX') + len('{{drugbox'):]
    #taxobox = taxobox[taxobox.index("\n[["):]
    taxobox = taxobox[:taxobox.index("}}")]

    taxobox = taxobox.replace('[[','')
    taxobox = taxobox.replace(']]','')
    taxobox = taxobox.replace('<br>','')
    taxobox = taxobox.replace("''",'')
    taxobox = taxobox.replace("&nbsp;",' ')

    t = []
    for i in taxobox.split("\n"):
        if len(i) > 0:
            if '|' in i:                    # for href titles
                t.append( i.split('|')[1] ) # for href titles
            else:
                t.append( i )

    return "\n".join(t)

page=wptools.page('paracetamol',lang='fr')
page.get_parse()
#print(page.data['infobox'])

def getDrugInfo(drug):
    page = wptools.page(drug)
    page.get_parse()
    #print(page.data['infobox'])

    result={}
    for i in page.data['infobox']:
        info =page.data['infobox'][i]
        info = info.replace('[[','')
        info = info.replace(']]','')
        info = info.replace("''", '')
        info = info.replace('<br>','')
        info = info.replace('&nbsp;',' ')

        result[i] = info

    print(result.keys())
    print(result.values())

getDrugInfo('paracetamol')
