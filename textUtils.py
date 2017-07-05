import re
import tldextract
import unicodedata
import traceback
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


def normalizeText(strIn):
    """
    """
    _normalized = unicodedata.normalize("NFKD", strIn)
    _ascii = _normalized.encode("ASCII", "ignore").decode()
    #fix translation errors
    _final=_ascii.replace("l<", "k").replace("|", "l")
    #clean string
    _cleanFinal=cleanRex.sub(_final," ")
    return _cleanFinal

def mineDomain(urlIn):
    """
    """
    extract=tldextract.TLDExtract(suffix_list_urls=None)
    _extract=extract(urlIn)
    _exObj=_extract.domain
    return _exObj

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

rexUr=re.compile(r"(?:[^@\s\/](?:[a-z0-9\-:]+)+\.){1,3}(?:[a-z]{2,4})", re.I)
rexDomain=re.compile(r"record\s+created", re.I)
cleanRex=re.compile(r"[\'\"\!\<\>\?\(\)\*%\$#`,;]")

def processFeatures(textIn):
    """
    this should suit each process need
    right now screenshots from known sites
    and whois records
    """
    #vars
    specialDict={}
    urls=[]

    #only headers text
    targetText=normalizeText(textIn[:150])
    try:
        rexUrls=rexUr.search(targetText)
        if rexUrls:
            url=rexUrls.group(0)
            print("## URL :", url)
            domain=mineDomain(url)
            specialDict["domain"]=domain
    except:
        print("[-] Fail to mine url")
        traceback.print_exc()
        print("[-] Fail to mine url\n")

    else:
        whois=[r for r in rexDomain.findall(textIn) if r]
        if whois:
            specialDict["domain"]="domaintools"
    return specialDict
