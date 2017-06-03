import re
import tldextract
from multiprocessing import Process, Manager

rexUr=re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
extract=tldextract.TLDExtract(suffix_list_urls=None)

def mineDomain(urlIn):
    """
    """
    _extract=extract(urlIn)
    _exObj=_extract.domain
    return _exObj

def buildRexList(valuesList):
    """
    """
    rexList=[]
    for values in valuesList:
        rex="\\b"+"\\b|\\b".join(values)+"\\b"
        rexList.append(re.compile(rex, re.I))
    return rexList

def doMacht(imageText, rexFunc, label, values, resultList):
    """
    """
    data={"label":label, "values":values, "match":[]}
    normValues=[v.strip().lower() for v in values if v]
    mets=[m for m in rexFunc.findall(imageText)
          if m.lower().strip() not in normValues]
    data["match"]=mets
    resultList.append(data)


def processCategories(imageText, subDirCats):
    """
    simple, very simple... just to start.
    """
    labels=list(subDirCats.keys())
    targetValues=list(subDirCats.values())
    rexFuncList=buildRexList(targetValues)
    manager=Manager()
    resultList=manager.list()
    processis=[]
    for n,rexFunc in enumerate(rexFuncList):
        _args=[imageText, rexFunc, labels[n],
               targetValues[n], resultList]
        p=Process(target=doMacht, args=_args)
        p.start()
        processis.append(p)
    for p in processis:p.join()
    return resultList


def processFeatures(textIn):
    """
    """
    fs={}
    urls=[url for url in rexUr.findall(textIn[:300]) if url]
    if not urls: return fs
    domains=[mineDomain(url) for url in urls]
    fs["domain"]=domains[0]
    if "l<" in fs["domain"]:
        fs["domain"]=fs["domain"].replace("l<", "k")
    return fs
