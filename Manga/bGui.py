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
        loadUi("bmd.ui",self)
        self.browseButton.clicked.connect(self.browsefiles)
        self.cancelButton.clicked.connect(sys.exit)
        self.downloadButton.clicked.connect(self.downloadChapters)
  
    def downloadChapters(self):
        self.download(3);

    def download(x):
        chapter = x
        url = f"https://readberserk.com/chapter/berserk-chapter-364-2/"
        directory = r'C:/Users/ripar/Documents/Coding/Python/Misc/Manga/'
        exportPath = r"C:/Users/ripar/Documents/Books/Berserk"
        r = requests.get(url)
        soup = bs(r.text, "html.parser")

        images = soup.find_all('img')

        images = [image for image in images if 'readberserk' in image['src']]
        # print(images)
        for index, image in enumerate(images):

            name = f'Berserk {chapter} {index}'
            source = image['src']
            
            print(f'Getting page #{index}...')
            with open(name.replace(' ','-') + '.jpg', 'wb') as f:
                im = requests.get(source)
                f.write(im.content)

        # Get images from BSoup
        inputFiles = [f'Berserk-{chapter}-{i}.jpg' for i in range(0, len(images))]
        print(inputFiles)
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
        print("Moved it")  

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