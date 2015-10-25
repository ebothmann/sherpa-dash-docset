#!/usr/local/bin/python

import os, re, sqlite3, urllib
from bs4 import BeautifulSoup, NavigableString, Tag 

db = sqlite3.connect('sherpa.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

sitepath = 'sherpa.docset/Contents/Resources/Documents/sherpa.hepforge.org'
docpath = os.path.join(sitepath, 'doc')
docpagepath = os.path.join(docpath,'SHERPA-MC-2.2.0.html')

page = open(docpagepath).read()
soup = BeautifulSoup(page)

any = re.compile('.*')

index_cp_tag = soup.find(class_="index-cp")

for tag in index_cp_tag.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 0:
        path = tag.attrs['href'].strip()
        if path.split('#')[0] == '' and path[0:7] == '#index-':
                # print 'name: %s, path: %s' % (name, path)
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Keyword', 'sherpa.hepforge.org/doc/SHERPA-MC-2.2.0.html'+path))

# Write TOC if needed
if soup.find('a', class_='dashAnchor') is None:

    heading_tag_re = re.compile('h[1-4]')
    heading_class_re = re.compile('(chapter|section|subsection|subsubsection|subsubheading)')
    for heading_tag in soup.find_all(heading_tag_re, class_=heading_class_re):
        # print(heading_tag.string)
        # print(urllib.quote(heading_tag.string.encode('utf8')))
        dash_anchor_tag = soup.new_tag("a",
                                       __name__="//apple_ref/cpp/Section/"+urllib.quote(heading_tag.string.encode('utf8'), ''),
                                       __class__="dashAnchor")
        # print(dash_anchor_tag)
        heading_tag.insert_before(dash_anchor_tag)


    soup_str = str(soup).replace(' __name__=', ' name=')  #.replace('"></a><h', '"></a><h')
    soup_str = soup_str.replace(' __class__=', ' class=')

    soup_str = soup_str.replace('href="/', 'href="../')
    
    open(docpagepath, mode='w').write(soup_str)

    open(os.path.join(sitepath, 'hepforge.css'), mode='a').write("\n.noprint {display:none}\n")

db.commit()
db.close()
