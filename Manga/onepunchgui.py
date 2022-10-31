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
        loadUi("OnePunchGui.ui", self)

        # Variables
        self.tempFolder = r'C:/Users/ripar/Documents/Coding/Python/Misc/Manga/'
        self.exportPath = r"C:/Users/ripar/Documents/Books/OnePunch/"
        self.mangaAbbrv = "Punch"
        self.pathText.setText(self.exportPath)

        # Connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.cancelButton.clicked.connect(sys.exit)
        self.downloadButton.clicked.connect(self.downloadChapters)

    def getMangaOnlyImages(self, imageList):
        return [img for img in imageList if img.has_attr('alt') and "One Punch" in img['alt']]


    def writeImages(self, chapter, imageList, nickName):
        for index, image in enumerate(imageList):
            name = f'{nickName}-{chapter}-{index}'
            source = image['src']
            
            print(f'...retrieving Pg #{index}...')
            with open(name.replace(' ','-') + '.jpg', 'wb') as f:
                im = requests.get(source)
                f.write(im.content)


    def browseFiles(self):
        # fname=QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', 'Images (*.png, *.xmp *.jpg)')
        fname = QFileDialog.getExistingDirectory(self, 'Open File')
        print(fname)
        self.pathText.setText(fname)


    def deleteTempImages(self, dir):
        x = os.listdir(dir)
        for img in x:
            if img.endswith(".jpg"):
                os.remove(os.path.join(dir, img))

    def downloadChapters(self):
        for i in range(self.startChapter.value(), self.endChapter.value() + 1):
            self.download(i)


    def download(self, chapter):

        url = f"https://ww1.onepunch.online/manga/onepunch-man-chapter-{chapter}/"
        r = requests.get(url)
        soup = bs(r.text, "html.parser")

        images = soup.find_all('img') # Get all images

        # Filter to only get imags in the manga itself
        images = self.getMangaOnlyImages(images)

        self.writeImages(chapter, images, self.mangaAbbrv)

        # List of Input file names
        inputFiles = [f'{self.mangaAbbrv}-{chapter}-{i}.jpg' for i in range(0, len(images))]
        # print(inputFiles)
        outputFile = open(f'{chapter}.pdf', 'wb')
        outputFile.write(converter.convert(inputFiles))
        outputFile.close()

        print("DONE Success")

        self.deleteTempImages(self.tempFolder)
        print("Deleted")
        # Move pdf to exportPath
        self.exportPath = self.pathText.text()
        shutil.move(f'{chapter}.pdf', self.exportPath)
        print(f"Moved chapter {chapter}")


app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1135)
widget.setFixedHeight(494)
widget.show()
sys.exit(app.exec_())