import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ImaginiReport:
    """
    """
    @staticmethod
    def _doLines(textIn, width=55):
        """
        """

        rangis=width-10
        textLen=len(textIn)
        splits=int(textLen/rangis)

        for n in range(1,splits+2):

            init=rangis*(n-1)
            end=rangis*n

            print("00000", n, init, end, textLen)

            if end > textLen:
                print("BREAAAAAKING", end, textLen)
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



    def saveData(self, fullData):
        """
        """
        ystart=750
        ypos=ystart
        self.canvas.drawString(10,ystart,"## IMAGE: {}".format(fullData["path"]))
        ypos-=20
        self.canvas.drawString(10,ypos,"## TEXT")
        for line in ImaginiReport._doLines(fullData["text"]):
            ypos-=15
            self.canvas.drawString(35,ypos,line)
            if ypos <= 40:
                self.canvas.showPage()
                ypos=730
        self.canvas.showPage()

    def close(self):
        """
        """
        self.canvas.save()
