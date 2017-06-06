import os, time
import datetime
import hashlib

from .textUtils import processCategories

def process_fileData(filePath):
    """
    """
    _data={}
    try:
        fileData = os.stat(filePath)
    except IOError:
        print ("[-] Failed to get information about:", filePath)
    else:
        dateMod=datetime.datetime.fromtimestamp(fileData.st_mtime)
        _data["modified_at"]=dateMod.strftime("%Y-%m-%d")
    return _data


def process_fileSystem(projectName, imageText, fileType, subDirCats, textFeat):
    """
    """
    #helpers
    def noCat():
        """
        """
        if textFeat is None: return os.path.join(projectName,newFileName)
        projFeat=os.path.join(projectName,textFeat)
        if not os.path.isdir(projFeat):os.mkdir(projFeat)
        return os.path.join(projectName,textFeat,newFileName)
    #file name
    hashis=hashlib.md5()
    hashis.update(imageText.encode())
    newFileName=hashis.hexdigest()+".jpg"
    #project directory test
    if not os.path.isdir(projectName):os.mkdir(projectName)
    #if there is no subdirectories by semantics
    if subDirCats is None: return noCat()
    #test semantics categories
    subsList=processCategories(imageText, subDirCats)
    labels=[o["label"] for o in subsList if o["match"]]
    #if not label, works as not sematincs categories
    if not labels:return noCat()
    #build filesystem for semantic categories
    catDir="_".join(labels)
    projCat=os.path.join(projectName,catDir)
    if not os.path.isdir(projCat):os.mkdir(projCat)
    #if no special textFeature
    if textFeat is None:return os.path.join(projCat, newFileName)
    #full path for full use of paramaters
    projFull=os.path.join(projectName,catDir,textFeat)
    if not os.path.isdir(projFull):os.mkdir(projFull)
    return os.path.join(projectName,catDir,textFeat,newFileName)
