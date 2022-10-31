from bs4 import BeautifulSoup as bs
import requests
import os
import img2pdf as converter 
import shutil


def download(x):
    chapter = x
    url = f"https://readberserk.com/chapter/berserk-chapter-364/"
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

# Input
start = int(input("Start chapter: "))
end = int(input("End chapter: "))
x=[]

# Pad chapters with 0s
for i in range(start, end + 1):
    if len(str(i)) == 2:
        x+=['0'+str(i)]
    elif len(str(i)) == 1:
        x+=['00'+str(i)]
    else:
        x+=[str(i)]

# for chap in x:
download(3)
