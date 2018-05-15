import urllib
import requests
from bs4 import BeautifulSoup
import re
import csv

def getPageContent(result):
    soup = BeautifulSoup(result.text, "lxml")
    tmp = soup.find(class_ = 'mw-content-ltr')
    keepBr = str(tmp)
    keepBr = keepBr.replace("<br/>", "^^")
    soup2 = BeautifulSoup(keepBr, "lxml")
    soup2 = str(soup2.text)
    final = soup2.replace("^^", "<br/>")
    for p in ponctuation:
         final = final.replace(p, ' ' + p + ' ')
    final = final.replace("\n", " ").replace("\t", " ")
    final = re.sub('\s+',' ', final)
    return final

# Adds a new content (newContent) to the page
def addContent(page, newContent):
    # Login request
    payload={'action':'query','format':'json','utf8':'','meta':'tokens','type':'login'}
    r1=requests.post(baseurl + 'api.php', data=payload)

    #login confirm
    login_token=r1.json()['query']['tokens']['logintoken']
    payload={'action':'login','format':'json','utf8':'','lgname':user,'lgpassword':passw,'lgtoken':login_token}
    r2=requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

    #get edit token2
    params3='?format=json&action=query&meta=tokens&continue='
    r3=requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
    edit_token=r3.json()['query']['tokens']['csrftoken']

    edit_cookie=r2.cookies.copy()
    edit_cookie.update(r3.cookies)

    payload={'action':'edit','assert':'user','format':'json','utf8':'','text':newContent,'summary':summary,'title':page,'token':edit_token}
    r4=requests.post(baseurl+'api.php',data=payload,cookies=edit_cookie)