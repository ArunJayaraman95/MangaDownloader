import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from bs4 import BeautifulSoup as bs
import requests
import os
import img2pdf as converter 
import shutil

class MainWindow(QDialog):
    
    
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("JojoGui.ui", self)
        self.label.setText("          Steel Ball Run Downloader")

        # Variables
        self.tempFolder = os.getcwd()
        self.exportPath = r"C:/SBR/"
        self.mangaAbbrv = "Jojo"
        self.defaultChapter = 1
        self.configFileName = "ConfigJojo.txt"
        self.alternator = True
        self.pathText.setText(self.exportPath)

        # Connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.cancelButton.clicked.connect(self.exit)
        self.downloadButton.clicked.connect(self.downloadChapters)
        self.startChapter.valueChanged.connect(self.startChanged)
        self.endChapter.valueChanged.connect(self.endChanged)

    def exit(self):
        """Writes config values and exits the GUI"""
        self.writeConfig()
        sys.exit()


    def startChanged(self):
        """Edits end chapter if start > end"""
        if self.startChapter.value() > self.endChapter.value():
            self.endChapter.setValue(self.startChapter.value())


    def endChanged(self):
        """Edits start chapter if start > end"""
        if self.startChapter.value() > self.endChapter.value():
            self.startChapter.setValue(self.endChapter.value())


    def getMangaOnlyImages(self, imageList: list):
        """Return images maching certain attributes"""
        # ? Debugging the HTML
        # for img in imageList:
        #     print(img.has_attr('id'))
        #     if img.has_attr('id'):
        #         print(img['id'])
        #         print("Src:", img['data-src'])
        # return []
        return [img for img in imageList if img.has_attr('src') and "blogspot" in img['src']]


    def writeImages(self, chapter: int, imageList: list, nickName: str):
        """Write image contents into jpg files"""
        pageCount = len(imageList)
        
        for index, image in enumerate(imageList):
            name = f'{nickName}-{chapter}-{index}'
            source = image['src']
            
            print(f'...retrieving Pg #{index}...')
            with open(name.replace(' ','-') + '.jpg', 'wb') as f:
                im = requests.get(source)
                f.write(im.content)
            self.pageLabel.setText(f"Page {index + 1} / {pageCount}")
            self.pageProgress.setValue((index + 1) * 100 // pageCount)


    def browseFiles(self):
        """Allow user to open file explorer and select a directory"""
        # fname=QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', 'Images (*.png, *.xmp *.jpg)')
        fname = QFileDialog.getExistingDirectory(self, 'Open File')
        print(fname)
        self.pathText.setText(fname)
        self.writeConfig()


    def deleteTempImages(self, dir: str):
        """Delete images in directory provided
        
        Args:
        dir -- Directory to delete imgs from
        """
        x = os.listdir(dir)
        for img in x:
            if img.endswith(".jpg"):
                os.remove(os.path.join(dir, img))

    # TODO: Make .exe file
    # TODO: Type checking
    def downloadChapters(self):
        """Download a range of chapters and update progress bars"""
        s,e = self.startChapter.value(), self.endChapter.value()
        self.chapterLabel.setText(f"Downloading Chapter 1 of {e - s + 1}")

        for i in range(self.startChapter.value(), self.endChapter.value() + 1):
            self.download(i)
            self.chapterLabel.setText(f"Downloading Chapter {i - s + 2} of {e - s + 1}")
            self.chapterProgress.setValue((i - s + 1) * 100 // (e - s + 1))

        self.chapterLabel.setText("ALL CHAPTERS DOWNLOADED")
        self.cancelButton.setText("Finish")
        self.writeConfig()


    def writeConfig(self):
        """Write exportPath and next chapter to config file"""
        f = open(self.configFileName, "w")
        
        self.exportPath = self.pathText.text()
        f.write(f'{self.exportPath}$$${str(self.endChapter.value() + 1)}')

        f.close()


    def readConfig(self):
        """Reads in configuration file and sets attributes in class"""
        if not os.path.exists(self.configFileName):
            return

        f = open(self.configFileName, "r")

        temp = f.read().split("$$$")
        self.exportPath = temp[0]
        self.defaultChapter = temp[1]

        self.pathText.setText(self.exportPath)
        self.startChapter.setValue(int(self.defaultChapter))
        self.endChapter.setValue(int(self.defaultChapter))

        f.close()


    def download(self, chapter: int):
        """Download a given chapter to export path with webscraping"""
        url = f"https://steel-ball-run.com/manga/jojos-bizarre-adventure-steel-ball-run-chapter-{chapter}/"
        r = requests.get(url)
        soup = bs(r.text, "html.parser")

        images = soup.find_all('img') # Get all images

        # Filter to only get imags in the manga itself
        images = self.getMangaOnlyImages(images)

        self.writeImages(chapter, images, self.mangaAbbrv)

        # List of Input file names
        inputFiles = [f'{self.mangaAbbrv}-{chapter}-{i}.jpg' for i in range(0, len(images))]
        outputFile = open(f'{chapter}.pdf', 'wb')
        outputFile.write(converter.convert(inputFiles))
        outputFile.close()

        print("DONE Success")

        self.deleteTempImages(self.tempFolder)
        print("Deleted")

        # Move pdf to exportPath
        self.exportPath = self.pathText.text()
        try:
            shutil.move(f'{chapter}.pdf', self.exportPath)
        except:
            os.remove(f'{chapter}.pdf')
            print("Chapter already exists")
        print(f"Moved chapter {chapter}")


app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1135)
widget.setFixedHeight(494)
widget.show()
sys.exit(app.exec_())