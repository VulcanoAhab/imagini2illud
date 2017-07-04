import traceback
import time
import shutil
import json
import os
import re

from .toText import process_screenShot
from .fileUtils import process_fileData, process_fileSystem
from .textUtils import processFeatures
from .report import ImaginiReport

class FileSequence:
    """
    """
    def __init__(self,filePath,projectName,subDirCats):
        """
        """
        self._data={
            "filePath":filePath,
            "projectName":projectName,
            "subDirCats":subDirCats,
            "index":0,
            "path":None,
        }


    @property
    def path(self):
        """
        """
        return self._data["path"]

    @property
    def data(self):
        """
        """
        return self._data

    @staticmethod
    def doTime(timeStart, timeEnd):
        """
        """
        duration=timeEnd-timeStart
        return "{:0.2f}".format(duration)


    def run(self):
        """
        """
        #image To Text
        ts=time.time()
        self._data["text"]=process_screenShot(self._data["filePath"])
        if not self._data["text"]:
            print("[-] No text: {}".format(self._data["filePath"]))
            return
        te=time.time()
        print("[+] toText took {}".format(FileSequence.doTime(ts,te)))
        #specialFeatures
        ts=time.time()
        self._data["specialFeatures"]=processFeatures(self._data["text"])
        te=time.time()
        print("[+] specialFeatures took {}".format(FileSequence.doTime(ts,te)))

        #file data
        ts=time.time()
        self._data["fileData"]=process_fileData(self._data["filePath"])
        te=time.time()
        print("[+] fileData took {}".format(FileSequence.doTime(ts,te)))

        #file name
        ts=time.time()
        fileType=self._data["filePath"].split("/")[-1].split(".")[-1]
        textFeatureCat=self._data["specialFeatures"].get("domain", None)
        self._data["path"]=process_fileSystem(self._data["projectName"],
                                            self._data["text"],
                                            fileType,
                                            self._data.get("subDirCats", None),
                                            textFeatureCat
                                            )
        #file move
        shutil.copy(self._data["filePath"], self._data["path"])
        te=time.time()
        print("[+] fileSytem took {}".format(FileSequence.doTime(ts,te)))
        #set to index
        self._data["index"]=1




class ProjectSequence:
    """
    """
    _rexIm=re.compile(r".{1,}\.(?:jpg|png|jpeg|tiff|gif)", re.I)

    def __init__(self, sourceDir, projectName):
        """
        """
        self.source=sourceDir
        self.proj=projectName
        self._catsData={}

    def add_category(self, catName, catValues):
        """
        """
        self._catsData.update({
            catName:catValues
        })

    def run(self, limitSize=None):
        """
        """
        filesString="\n".join(os.listdir(self.source))
        files=self._rexIm.findall(filesString)
        #pdf canvas
        fileName="_".join([self.proj, "report.pdf"])
        imDex=ImaginiReport(self.proj, fileName)
        if limitSize:
            files=files[:limitSize]
        for f in files:
            newFile=None
            newData={}
            filePath=os.path.join(self.source, f)

            print("[+] Starting to process image: {}".format(filePath))

            try:
                seq=FileSequence(filePath, self.proj, self._catsData)
                seq.run()
                if not seq.path:
                    print("No pathis")
                    continue
                newFile=seq.path
                newData=seq.data
                imDex.saveData(newData)
            except Exception as e:
                print("[-] Fail to process image: {}".format(filePath))
                traceback.print_exc()
                continue
            print("[+] Finished processing image: {}".format(newFile))
        #save pdf
        imDex.close()
        print("[+] Done mapping images and producing report")
