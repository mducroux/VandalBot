import urllib
import requests
from bs4 import BeautifulSoup
import re
import csv

baseurl='http://wikipast.epfl.ch/wikipast/'

fullbios = ''
name = 'Biographies'
result=requests.post(baseurl+'api.php?action=query&titles='+name+'&export&exportnowrap')
soup=BeautifulSoup(result.text, "lxml")
code=''
for primitive in soup.findAll("text"):
    code+=primitive.string
fullbios = code

users2018 = open("liste_utilisateurs_2018.txt", "r")
lines = users2018.readlines()
list_users_2018 = [l.strip('\n') for l in lines]

users2017 = open("liste_utilisateurs_2017.txt", "r")
lines = users2017.readlines()
list_users_2017 = [l.strip('\n') for l in lines]

goodBots = open("list_good_bots.txt", "r")
lines = goodBots.readlines()
list_good_bots = [l.strip('\n') for l in lines]

protected_logins = list(set(list_users_2018).union(set(list_users_2017)))

def getPageList(logins):
    liste_pages=[]
    for user in logins:
        result=requests.post(baseurl+'api.php?action=query&list=usercontribs&ucuser='+user+'&format=xml')
        soup=BeautifulSoup(result.content,'lxml')
        for primitive in soup.usercontribs.findAll('item'):
            liste_pages.append(primitive['title'])
    liste_pages=list(set(liste_pages))
    return liste_pages

humansPages = getPageList(protected_logins)

protected_logins = list(set(list_users_2018).union(set(list_users_2017)).union(set(list_good_bots)))

def getRandomPage():
    result=requests.post(baseurl+'index.php/Special:Page_au_hasard')
    return result.url[43:]

botsPages = []
while(len(botsPages) < len(humansPages)):
    tmp = getRandomPage()
    if((tmp not in humansPages) and (tmp not in botsPages) and len(tmp) > 20):
        botsPages.append(tmp)

ponctuation = ['!','?',',',"'","\"",'(',')', '[', ']', '{', '}', ';', ':', '<br/>', '...', '. ']

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

humansTextPages = []
for p in humansPages:
    result = requests.post(baseurl+'index.php/'+p)
    humansTextPages.append(getPageContent(result) + "\t0")

botsTextPages = []
for p in botsPages:
    result = requests.post(baseurl+'index.php/'+p)
    botsTextPages.append(getPageContent(result) + "\t1")

textPagesPlusIndicator = list(set(humansTextPages).union(set(botsTextPages)))

file = open('output.txt','w')
for item in textPagesPlusIndicator:
    file.write("%s\n" % item)