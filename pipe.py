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

    def run(self):
        """
        """
        #image To Text
        self._data["text"]=process_screenShot(self._data["filePath"])
        if not self._data["text"]:
            print("[-] No text: {}".format(self._data["filePath"]))
            return
        #specialFeatures
        self._data["specialFeatures"]=processFeatures(self._data["text"])
        #file data
        self._data["fileData"]=process_fileData(self._data["filePath"])
        #file name
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

    def run(self):
        """
        """
        filesString="\n".join(os.listdir(self.source))
        files=self._rexIm.findall(filesString)
        #pdf canvas
        fileName="_".join([self.proj, "report.pdf"])
        imDex=ImaginiReport(self.proj, fileName)

        for f in files:

            newFile=None
            newData={}
            filePath=os.path.join(self.source, f)

            try:
                seq=FileSequence(filePath, self.proj, self._catsData)
                seq.run()
                if not seq.path:continue
                newFile=seq.path
                newData=seq.data
                imDex.saveData(newData)
            except Exception as e:
                print("[-] Fail to process image: {}".format(filePath))
                print("    Error:", e)
                continue

            print("[+] Finished processing image: {}".format(newFile))

        #save pdf
        imDex.close()
        print("[+] Done mapping images and producing report")
