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
        super(MainWindow,self).__init__()
        loadUi("opmd.ui",self)
        self.browseButton.clicked.connect(self.browsefiles)
        self.cancelButton.clicked.connect(sys.exit)
        self.downloadButton.clicked.connect(self.downloadChapters)

    def downloadChapters(self):
        start = self.startChapter.value()
        end = self.endChapter.value()
        path = self.pathText.text()

        print(start, end,path)
        # self.download(start, path)
        print(f"Downloading {start} to {path}")

        chapter = start
        print(f"Downloading {chapter} to {path}")
        url = f"https://ww5.manganelo.tv/chapter/manga-aa951409/chapter-{chapter}"
        directory = path + "/temp/"
        exportPath = path
        r = requests.get(url)
        soup = bs(r.text, "html.parser")

        images = soup.find_all('img') # Get all images

        # Filter to only get images in the manga itself
        images = [image for image in images if image.has_attr('title') and "One Piece" in image['title']]

        # print(images[6], type(images[6]), images[6]['title'])
        for index, image in enumerate(images):

            name = f'OP-{chapter}-{index}'
            source = image['data-src']
            
            print(f'...retrieving Pg #{index}...')
            with open(name.replace(' ','-') + '.jpg', 'wb') as f:
                im = requests.get(source)
                f.write(im.content)

        # Get images from BSoup
        inputFiles = [f'OP-{chapter}-{i}.jpg' for i in range(0, len(images))]
        # print(inputFiles)
        outputFile = open(f'{chapter}.pdf', 'wb')
        outputFile.write(converter.convert(inputFiles))
        outputFile.close()
        print("DONE Success")
        test = os.listdir(directory)
        for images in test:
            if images.endswith(".jpg"):
                os.remove(os.path.join(directory, images))
        # print(chapter)
        shutil.move(f'{chapter}.pdf', exportPath)
        os.remove(directory)
        print("Moved it")    

    def downloader(chapter, path):
        # TODO: Put TRY EXCEPT on this block of code
        print(f"Downloading {chapter} to {path}")
        url = f"https://ww5.manganelo.tv/chapter/manga-aa951409/chapter-{chapter}"
        directory = path + "/temp/"
        exportPath = path
        # r = requests.get(url)
        # soup = bs(r.text, "html.parser")

        # images = soup.find_all('img') # Get all images

        # # Filter to only get images in the manga itself
        # images = [image for image in images if image.has_attr('title') and "One Piece" in image['title']]

        # # print(images[6], type(images[6]), images[6]['title'])
        # for index, image in enumerate(images):

        #     name = f'OP-{chapter}-{index}'
        #     source = image['data-src']
            
        #     print(f'...retrieving Pg #{index}...')
        #     with open(name.replace(' ','-') + '.jpg', 'wb') as f:
        #         im = requests.get(source)
        #         f.write(im.content)

        # # Get images from BSoup
        # inputFiles = [f'OP-{chapter}-{i}.jpg' for i in range(0, len(images))]
        # # print(inputFiles)
        # outputFile = open(f'{chapter}.pdf', 'wb')
        # outputFile.write(converter.convert(inputFiles))
        # outputFile.close()
        # print("DONE Success")
        # test = os.listdir(directory)
        # for images in test:
        #     if images.endswith(".jpg"):
        #         os.remove(os.path.join(directory, images))
        # # print(chapter)
        # shutil.move(f'{chapter}.pdf', exportPath)
        # os.remove(directory)
        # print("Moved it")    

    def browsefiles(self):
        # fname=QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', 'Images (*.png, *.xmp *.jpg)')
        fname = QFileDialog.getExistingDirectory(self, 'Open File')
        print(fname)
        self.pathText.setText(fname)

app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1135)
widget.setFixedHeight(494)
widget.show()
sys.exit(app.exec_())