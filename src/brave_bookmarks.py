#!/usr/bin/python
import json
import os

from Alfred import Items as Items
from Alfred import Tools as Tools


def list_dict_sort(seq, key, reverse=False):
    return sorted(seq, key=lambda k: k[key], reverse=reverse)


wf = Items()

user_dir = os.path.expanduser('~')
bookmarks_file = user_dir + '/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks'

with open(bookmarks_file,'r') as bm_file:
    bm_json = json.load(bm_file)['roots']

bookmarks = list()
for key, folder in bm_json.items():
    for children in folder['children']:
        bookmarks.append({
            'name': children['name'],
            'url': children['url']})

bookmarks = list_dict_sort(bookmarks,'name')

for bm in bookmarks:
    name = bm['name']
    url = bm['url']

    wf.setItem(
        title=name,
        subtitle=url,
        arg=url,
        quicklookurl=url
    )
    wf.addItem()

wf.write()