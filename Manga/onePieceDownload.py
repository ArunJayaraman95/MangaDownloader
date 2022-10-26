from bs4 import BeautifulSoup as bs
import requests
import os
import img2pdf as converter 
import shutil

def getMangaOnlyImages(imageList):
    return [img for img in imageList if img.has_attr('title') and "One Piece" in img['title']]

def writeImages(chapter, imageList):
    for index, image in enumerate(imageList):
        name = f'OP-{chapter}-{index}'
        source = image['data-src']
        
        print(f'...retrieving Pg #{index}...')
        with open(name.replace(' ','-') + '.jpg', 'wb') as f:
            im = requests.get(source)
            f.write(im.content)

def download(chapter):

    url = f"https://ww5.manganelo.tv/chapter/manga-aa951409/chapter-{chapter}"
    directory = r'C:/Users/ripar/Documents/Coding/Python/Misc/Manga/'
    exportPath = r"C:/Users/ripar/Documents/Books/OnePiece/"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")

    images = soup.find_all('img') # Get all images

    # Filter to only get images in the manga itself
    images = getMangaOnlyImages(images)

    writeImages(chapter, images)

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
    print("Moved it")

# Input
start = int(input("Start chapter: "))
end = int(input("End chapter: "))
x=[]

# Pad chapters with 0s
for i in range(start, end + 1):
    x+=[str(i)]

for chap in x:
    download(chap)
