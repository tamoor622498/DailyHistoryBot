import os  # Downloads and deletes the file.
import wikipedia  # Finds the images
import requests  # to sent GET requests
from bs4 import BeautifulSoup  # to parse HTML
import re  # regex expressions
import random


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

        # searchResults = wikipedia.search(imageLinks[0].replace('/wiki/', ''))
        searchResults = imageLinks
        # Found results for wikiPage query

        if len(searchResults) == 0:
            return False
        # if no search results come up.

        imagePage = None
        imgIndex = 0
        while imgIndex < len(searchResults) and imagePage == None:
            try:
                imagePage = wikipedia.page(searchResults[imgIndex].replace('/wiki/', ''))
            except:
                if imagePage == None:
                    imgIndex += 1
        # Iterates through the list until it finds a viable page to search for an image.

        if len(imagePage.images) == 0 or imagePage == False:
            return False
        # If no images are found on the page

        unfilteredMedia = imagePage.images
        # All media on the page.

        acceptedFormats = ['JPG', 'PNG', 'GIF', 'WEBP', 'jpg', 'png', 'gif', 'webp']
        # Image formats accepted by twitter

        posImages = []
        for i in range(len(unfilteredMedia)):
            if unfilteredMedia[i][len(unfilteredMedia[i]) - 3:len(unfilteredMedia[i])] in acceptedFormats:
                posImages.append(unfilteredMedia[i])
        # Filters out invalid file extensions

        if len(posImages) == 0:
            return False
        # If all images were invalid

        requestedImage = posImages[random.randrange(0, len(posImages))]
        image = requests.get(requestedImage)
        fileExtension = requestedImage[len(requestedImage) - 4:len(requestedImage)]
        # Grabs a random image file link and the file extension.

        self.imageName = "img" + fileExtension
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


# def main():
#     currDate = datetime.now()
#     month = currDate.strftime("%B")
#     currDay = currDate.day
#
#     t = ImageDownload(month, currDay)
#     x = t.download(30)
#     t.deleteImage(x)
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
# if __name__ == '__main__':
#     main()
