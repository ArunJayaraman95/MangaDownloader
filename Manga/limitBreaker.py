from bs4 import BeautifulSoup as bs
import requests
import os
import img2pdf as converter 
import shutil

def getMangaOnlyImages(imageList):
    return [img for img in imageList if img.has_attr('src') and "limit" in img['src']]


def writeImages(chapter, imageList, nickName):
    for index, image in enumerate(imageList):
        name = f'{nickName}-{chapter}-{index}'
        source = image['src']
        
        print(f'...retrieving Pg #{index}...')
        with open(name.replace(' ','-') + '.jpg', 'wb') as f:
            im = requests.get(source)
            f.write(im.content)


def deleteTempImages(dir):
    x = os.listdir(dir)
    for img in x:
        if img.endswith(".jpg"):
            os.remove(os.path.join(dir, img))

def download(chapter):

    url = f"https://limit-breaker.online/manga/limit-breaker-chapter-{chapter}/"
    tempFolder = r'C:/Users/ripar/Documents/Coding/Python/Misc/Manga/'
    exportPath = r"C:/Users/ripar/Documents/Books/LimitBreaker/"
    mangaAbbrv = "LimBrkr"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")

    images = soup.find_all('img') # Get all images

    # Filter to only get imags in the manga itself
    images = getMangaOnlyImages(images)

    writeImages(chapter, images, mangaAbbrv)

    # List of Input file names
    inputFiles = [f'{mangaAbbrv}-{chapter}-{i}.jpg' for i in range(0, len(images))]
    # print(inputFiles)
    outputFile = open(f'{chapter}.pdf', 'wb')
    outputFile.write(converter.convert(inputFiles))
    outputFile.close()

    print("DONE Success")

    deleteTempImages(tempFolder)
    print("Deleted")
    # Move pdf to exportPath
    shutil.move(f'{chapter}.pdf', exportPath)
    print(f"Moved chapter {chapter}")

# Input
start = int(input("Start chapter: "))
end = int(input("End chapter: "))

for chap in [str(i) for i in range(start, end + 1)]:
    download(chap)
