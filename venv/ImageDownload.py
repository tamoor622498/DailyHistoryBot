import os  # Downloads and deletes the file.
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
        self.saveFolder = "MEDIA"

    def download(self, index):
        if not os.path.exists(self.saveFolder):
            os.mkdir(self.saveFolder)
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

        # posImagePages = wikipedia.search(imageLinks[0].replace('/wiki/', ''))
        posImagePages = imageLinks
        # Found results for wikiPage query

        if len(posImagePages) == 0:
            return False
        # if no search results come up.

        response = requests.get("https://en.wikipedia.org" + posImagePages[0])
        html = response.text
        # Gets the HTML for the page

        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find("a", class_="image")
        # Finds all of the links with image class

        try:
            allImagesOnPage = [img for img in results.select('img')]
            # all of the images in the "a" tags
        except:
            return False;

        requestedImage = allImagesOnPage[0]['src']
        # gets the src of each image

        requestedImage = "https:" + requestedImage.replace(
            requestedImage[requestedImage.find("px") - 3:requestedImage.find("px")], "1000")
        # remakes the links so the image is 1000px high

        image = requests.get(requestedImage)
        fileExtension = requestedImage[len(requestedImage) - 4:len(requestedImage)]
        # Grabs a random image file link and the file extension.

        self.imageName = "tweetImage" + fileExtension
        # The file name
        imageLoc = self.saveFolder + '/' + self.imageName
        # Path to file
        with open(imageLoc, 'wb') as file:
            file.write(image.content)
        # The file downloaded and saved

        return imageLoc

    def deleteImage(self, imageLoc):
        if imageLoc:
            print("DELETING: " + imageLoc)
            os.remove(imageLoc)
        # Deletes the image through exact file path.


def main():
    currDate = datetime.now()
    month = currDate.strftime("%B")
    currDay = currDate.day

    t = ImageDownload(month, currDay)
    x = t.download(2)
    # t.deleteImage(x)


#     # l = []
#     # for i in range(40):
#     #     print("TIMES: " + str(i))
#     #     l.append(t.download(i))
#     #
#     # time.sleep(10)
#     #
#     # for k in range(len(l)):
#     #     if l[k]:
#     #         t.deleteImage(l[k])
#
#
if __name__ == '__main__':
    main()
