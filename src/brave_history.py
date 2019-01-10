#!/usr/bin/python

from Alfred import Items as Items
from Alfred import Tools as Tools
import sqlite3
import shutil
import os
import urlparse
import sys


def removeDuplicates(li):
    prev = str()
    newList = list()
    for i in li:
        cur = i[0]
        if prev != cur:
            newList.append(i)
            prev = cur
    return newList


def filterResults(li,term):
    if term != '':
        newList = list()
        for i in li:
            if term.lower() in i[1].lower():
                newList.append(i)
    else:
        newList = li
    return newList

def filterHostname(li):
    newList = list()
    prev_host = str()
    for i in li:
        o = urlparse.urlparse(i[0])
        cur_host = o.hostname
        if prev_host != cur_host:
            newList.append(i)
            prev_host = cur_host
    return newList


wf = Items()

search_term = Tools.getArgv(1) if Tools.getArgv(1) is not None else ''

user_dir = os.path.expanduser('~')
chrome_locked_db = user_dir + '/Library/Application Support/BraveSoftware/Brave-Browser/Default/History'
history_db = '/tmp/History'

try:
    shutil.copy2(chrome_locked_db, '/tmp')
except IOError:
    wf.setItem(
        title="Brave Browser History not found!",
        subtitle="You may use an older version of Brave or no Brave",
        valid=False
    )
    wf.addItem()
    wf.write()
    exit()

c = sqlite3.connect(history_db)
cursor = c.cursor()
select_statement = "SELECT urls.url, urls.title, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(select_statement)
results = cursor.fetchall()

os.remove(history_db)

results = removeDuplicates(results)
results = filterResults(results,search_term)
results = filterHostname(results)

if len(results) > 0:
    for i in results:
        url = i[0]
        title = i[1]
        visits = i[2]
        wf.setItem(
            title=title,
            subtitle="%s Visits: %s" % (url,str(visits)),
            arg=url
        )
        wf.addItem()
else:
    wf.setItem(
        title="Nothing found in History!",
        subtitle="Try again...",
        valid=False
    )
    wf.addItem()
wf.write()
