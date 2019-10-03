#!/usr/bin/python
import json
import os

from Alfred import Items as Items
from Alfred import Tools as Tools

BRAVE_BOOKMARKS = '/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks'
BRAVE_DEV_BOOKMARKS = '/Library/Application Support/BraveSoftware/Brave-Browser-Dev/Default/Bookmarks'


def get_all_urls(the_json):
    def extract_data(data):
        if data.get('type') == 'url':
            urls.append({'name': data['name'], 'url': data['url']})
        if data.get('type') == 'folder':
            the_children = data['children']
            get_container(the_children)

    def get_container(o):
        if isinstance(o, list):
            for i in o:
                extract_data(i)
        if isinstance(o, dict):
            for k, i in o.items():
                extract_data(i)
    urls = list()
    get_container(the_json)
    return sorted(urls, key=lambda k: k['name'], reverse=False)


def path_to_bookmarks():
    user_dir = os.path.expanduser('~')
    bm = user_dir + BRAVE_BOOKMARKS
    bm_dev = user_dir + BRAVE_DEV_BOOKMARKS
    if os.path.isfile(bm):
        return bm
    elif os.path.isfile(bm_dev):
        return bm_dev


def get_json_from_file(file):
    with open(file, 'r') as bm_file:
        return json.load(bm_file)['roots'].encode('utf-8')


wf = Items()
query = Tools.getArgv(1) if Tools.getArgv(1) is not None else str()
bookmarks_file = path_to_bookmarks()

if bookmarks_file is not None:
    bm_json = get_json_from_file(bookmarks_file)
    bookmarks = get_all_urls(bm_json)
    for bm in bookmarks:
        name = bm.get('name')
        url = bm.get('url')
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
else:
    wf.setItem(
        title="Bookmark File not found!",
        subtitle='Ensure Brave is installed',
        valid=False
    )
    wf.addItem()

wf.write()
