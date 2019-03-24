#!/usr/bin/python
import json
import os

from Alfred import Items as Items


def get_all_urls(the_json):
    def get_container(o):
        if isinstance(o, list):
            for i in o:
                if i['type'] == 'url':
                    urls.append({'name': i['name'], 'url': i['url']})
                if i['type'] == 'folder':
                    the_children = i['children']
                    get_container(the_children)
        if isinstance(o, dict):
            for k,j in o.items():
                t = j['type']
                if t == 'url':
                    urls.append({'name': j['name'], 'url': j['url']})
                if t == 'folder':
                    the_children = j['children']
                    get_container(the_children)
    urls = list()
    get_container(the_json)
    return sorted(urls, key=lambda k: k['name'], reverse=False)


wf = Items()

user_dir = os.path.expanduser('~')
bookmarks_file = user_dir + '/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks'

with open(bookmarks_file,'r') as bm_file:
    bm_json = json.load(bm_file)['roots']

bookmarks = get_all_urls(bm_json)

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
