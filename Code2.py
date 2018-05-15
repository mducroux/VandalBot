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
    final = final.replace('\s+','\s')
    return final

