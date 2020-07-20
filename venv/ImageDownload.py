import os  # Dowwloads and deletes the file.
import wikipedia  # Finds the images
import requests  # to sent GET requests
from bs4 import BeautifulSoup  # to parse HTML
import re  # regex expressions

import random

from datetime import datetime


class ImageDownload:
    def __init__(self, month, day):
        self.month = month
        self.day = day

    def download(self, index):
        saveFolder = "MEDIA"
        if not os.path.exists(saveFolder):
            os.mkdir(saveFolder)
        # Creates folder to store image.

        pageURl = "https://en.wikipedia.org/wiki/" + self.month + "_" + str(self.day)
        # HTML to download.

        response = requests.get(pageURl)
        html = response.text
        # Raw HTML for the page.

        soup = BeautifulSoup(html, 'html.parser')
        lists = [ul for ul in soup.select('ul')]
        # Extracts all of the il tags on the page.

        eventList = [li for li in lists[1].select('li')]
        # Extracts the list of events (the second ul tag).

        imageLinks = [a['href'] for a in eventList[index].select('a[href]')]
        # Extracts the image links from a specified index on the list.
        # If it was just "a" instead of "a['href']" at the start, it would get whole tag.

        imageTitles = [a['title'] for a in eventList[index].select('a[title]')]
        # Gets the titles used for images

        if len(imageLinks) == 0:
            return False
        # If there are no links in the event to search for images.

        if re.match(r'[0-9]', imageTitles[0]) or "AD " in imageTitles[0]:
            imageLinks.pop(0)
            imageTitles.pop(0)
        # Removes the page for the whole year
        # .

        searchResults = wikipedia.search(imageLinks[0].replace('/wiki/', ''))
        # Found results for wikiPage query

        if len(searchResults) == 0:
            return False
        # if no search results come up.

        imagePage = None
        imgIndex = 0
        while imgIndex < len(searchResults) and imagePage == None:
            try:
                imagePage = wikipedia.page(searchResults[imgIndex])
            except:
                if imagePage == None:
                    imgIndex += 1
        # Iterates through the list until it finds a viable page to search for an image.

        if len(imagePage.images) == 0:
            return False
        # If no images are found on the page

        image = requests.get(imagePage.images[0])
        fileExtension = imagePage.images[0][len(imagePage.images[0])-4:len(imagePage.images[0])]

        imageName = saveFolder + '/' + "img" + str(random.randrange(0, 10000)) + fileExtension
        with open(imageName, 'wb') as file:
            file.write(image.content)

        return True

        # if not re.match(r'^([\s\d]+)$', imageTitles[0]):
        #     pageID = imageLinks[0].replace('/wiki/', '')
        #     # imagePage = wikipedia.page(pageID)
        # else:
        #     pageID = imageLinks[1].replace('/wiki/', '')
        #     #imagePage = wikipedia.page(pageID)
        # # Filters out the page for years, gets part of the event.
        #
        # print(pageID)
        # print(wikipedia.page(pageID,auto_suggest=True, redirect=True))
        # print(wikipedia.page(wikipedia.search(pageID)[0]).images)

    def deleteImage(self):
        pass


def main():
    currDate = datetime.now()
    month = currDate.strftime("%B")
    currDay = currDate.day

    t = ImageDownload(month, currDay+1)
    # t.download(30)
    for i in range(20):
        print("TIMES: " + str(i))
        t.download(i)


if __name__ == '__main__':
    main()
