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
        _data["modified_at"]=datetime.datetime.fromtimestamp(fileData.st_mtime)
    return _data


def process_fileSystem(projectName, imageText, fileType, subDirCats, textFeat):
    """
    """
    hashis=hashlib.md5()
    hashis.update(imageText.encode())
    newFileName=hashis.hexdigest()+".jpg"
    if not os.path.isdir(projectName):os.mkdir(projectName)
    if subDirCats is None:
        if textFeat is None: return os.path.join(projectName,newFileName)
        projFeat=os.path.join(projectName,textFeat)
        if not os.path.isdir(projFeat):os.mkdir(projFeat)
        return os.path.join(projectName,textFeat,newFileName)
    subsList=processCategories(imageText, subDirCats)
    labels=[o["label"] for o in subsList]
    catDir="_".join(labels)
    if textFeat is None: return os.path.join(projectName, catDir, newFileName)
    projFull=os.path.join(projectName,catDir,textFeat)
    projCat=os.path.join(projectName,catDir)
    if not os.path.isdir(projCat):os.mkdir(projCat)
    if not os.path.isdir(projFull):os.mkdir(projFull)
    return os.path.join(projectName,catDir,textFeat,newFileName)
