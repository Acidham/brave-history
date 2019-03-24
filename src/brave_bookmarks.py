#!/usr/bin/python
import json
import os

from Alfred import Items as Items
from Alfred import Tools as Tools


def get_all_urls(the_json):
    def extract_data(data):
        if data['type'] == 'url':
            urls.append({'name': data['name'], 'url': data['url']})
        if data['type'] == 'folder':
            the_children = data['children']
            get_container(the_children)

    def get_container(o):
        if isinstance(o, list):
            for i in o:
                extract_data(i)
        if isinstance(o, dict):
            for k,i in o.items():
                extract_data(i)
    urls = list()
    get_container(the_json)
    return sorted(urls, key=lambda k: k['name'], reverse=False)


wf = Items()
query = Tools.getArgv(1) if Tools.getArgv(1) is not None else str()
user_dir = os.path.expanduser('~')
bookmarks_file = user_dir + '/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks'

with open(bookmarks_file,'r') as bm_file:
    bm_json = json.load(bm_file)['roots']

bookmarks = get_all_urls(bm_json)

for bm in bookmarks:
    name = bm['name']
    url = bm['url']
    if query == str() or query.lower() in name.lower():
        wf.setItem(
            title=name,
            subtitle=url,
            arg=url,
            quicklookurl=url
        )
        wf.addItem()

if wf.getItemsLengths() == 0:
    wf.setItem(
        title='No Bookmark found!',
        subtitle='Search \"%s\" in Google...' % query,
        arg='https://www.google.com/search?q=%s' % query
    )
    wf.addItem()

wf.write()
