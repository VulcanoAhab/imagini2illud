import re
import tldextract
from multiprocessing import Process, Manager



def buildRexList(valuesList):
    """
    """
    rexList=[]
    for values in valuesList:
        rex="\\b"+"\\b|\\b".join([re.escape(v) for v in values])+"\\b"
        rexList.append(re.compile(rex, re.I))
    return rexList

def doMacht(imageText, rexFunc, label, values, resultList):
    """
    """
    data={"label":label, "values":values, "match":[]}
    normValues=[v.strip().lower() for v in values if v]
    mets=[m for m in rexFunc.findall(imageText)
          if m.lower().strip() in normValues]
    data["match"]=mets
    resultList.append(data)


def processCategories(imageText, subDirCats):
    """
    simple, very simple... just to start.
    """
    labels=list(subDirCats.keys())
    targetValues=[subDirCats[label] for label in labels]
    rexFuncList=buildRexList(targetValues)
    # manager=Manager()
    # resultList=manager.list()
    #processis=[]
    resultList=[]
    for n,rexFunc in enumerate(rexFuncList):
        _args=[imageText, rexFunc, labels[n],
               targetValues[n], resultList]
        doMacht(*_args)
    #     p=Process(target=doMacht, args=_args)
    #     p.start()
    #     processis.append(p)
    # for p in processis:p.join()
    return resultList


### ----
#helpers

rexUr=re.compile(r"([^@](?:(?:[a-z0-9\-:]+)+\.)(?:[a-z]{2,4}))\/\S+", re.I)
rexDomain=re.compile(r"record\s+created", re.I)

def processFeatures(textIn):
    """
    this should suit each process need
    right now screenshots from known sites
    and whois records
    """
    #vars
    specialDict={}

    #helpers
    # rexUr=re.compile(r"([^@](?:(?:[a-z0-9\-:]+)+\.)(?:[a-z]{2,4}))\/\S+", re.I)
    # rexDomain=re.compile(r"record\s+created", re.I)

    def mineDomain(urlIn):
        """
        """
        extract=tldextract.TLDExtract(suffix_list_urls=None)
        _extract=extract(urlIn)
        _exObj=_extract.domain
        return _exObj

    #only headers text
    targetText=textIn[:150].replace("l<", "k").replace("|", "BAR")
    print("\nTARGET TEXT", targetText)
    features=rexUr.findall(targetText)
    print("FEARTURES", features)
    urls=[url for url in features  if url]
    if not urls:
        whois=[r for r in rexDomain.findall(textIn) if r]
        if whois:
            specialDict["domain"]="domaintools"
        return specialDict
    domains=[mineDomain(url) for url in urls]

    #test result
    if (len(domains[0]) <= 3
        or domains[0].replace(".","").isdigit()):
        return specialDict
    specialDict["domain"]=domains[0]
    return specialDict
