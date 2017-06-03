import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ImaginiReport:
    """
    """
    @staticmethod
    def _doLines(textIn, width=75):
        """
        """

        rangis=width-10
        textLen=len(textIn)
        splits=int(textLen/rangis)

        for n in range(1,splits+2):

            init=rangis*(n-1)
            end=rangis*n
            if end > textLen:
                end=textLen
                yield textIn[init:end]
                break

            yield textIn[init:end]

    def __init__(self, projName, filePath):
        """
        """
        self.proj=projName
        self.path=filePath
        self.canvas=canvas.Canvas(self.path, pagesize=letter)
        self.canvas.setFont('Helvetica', 10)


    def _prepare_forItem(self, yPosition, lineSize=15):
        """
        """
        yPosition-=lineSize
        if yPosition <= 40:
            self.canvas.showPage()
            yPosition=730
        return yPosition

    def saveData(self, fullData):
        """
        """
        yStart=750
        yPos=yStart
        xTitle=10
        xIdent1=20

        imgMsg="## Image: {}".format(fullData["path"])
        self.canvas.drawString(xTitle,yStart,imgMsg)
        yPos=self._prepare_forItem(yPos, lineSize=30)

        self.canvas.drawString(xTitle,yPos,"## Text")
        for line in ImaginiReport._doLines(fullData["text"]):
            yPos=self._prepare_forItem(yPos)
            self.canvas.drawString(xIdent1,yPos,line)

        yPos=self._prepare_forItem(yPos,lineSize=30)
        self.canvas.drawString(xTitle,yPos,"## Modified_at")
        yPos=self._prepare_forItem(yPos)
        modAt=fullData["fileData"].get("modified_at")
        self.canvas.drawString(xIdent1,yPos,modAt)

        self.canvas.showPage()

    def close(self):
        """
        """
        self.canvas.save()
