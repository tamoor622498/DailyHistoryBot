import os  # Downloads and deletes the file.
import wikipedia  # Finds the images
import requests  # to sent GET requests
from bs4 import BeautifulSoup  # to parse HTML
import re  # regex expressions
import random
from datetime import datetime


class ImageDownload:
    def __init__(self, page):
        # self.month = month
        # self.day = day
        self.page = page
        self.saveFolder = "MEDIA"

    def download(self, index):
        if not os.path.exists(self.saveFolder):
            os.mkdir(self.saveFolder)
        # Creates folder to store image.

        # pageURl = "https://en.wikipedia.org/wiki/" + self.month + "_" + str(self.day)
        # # HTML to download.
        #
        # response = requests.get(pageURl)
        # html = response.text
        # # Raw HTML for the page.

        soup = BeautifulSoup(self.page, 'html.parser')
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

        print(imageTitles)
        response = requests.get("https://en.wikipedia.org" + posImagePages[0])
        html = response.text
        # Gets the HTML for the page

        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find("a", class_="image")
        # Finds all of the links with image class

        try:
            allImagesOnPage = [img for img in results.select('img')]
            allImagesOnPage = soup.findAll('img')
            # all of the images in the "a" tags
        except:
            return False

        ignore = {"//upload.wikimedia.org/wikipedia/en/thumb/9/99/Question_book-new.svg/50px-Question_book-new.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/9/94/Symbol_support_vote.svg/19px-Symbol_support_vote.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Text_document_with_red_question_mark.svg/40px-Text_document_with_red_question_mark.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/b/b4/Ambox_important.svg/40px-Ambox_important.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Crystal_Clear_app_kedit.svg/40px-Crystal_Clear_app_kedit.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/e/e7/Cscr-featured.svg/20px-Cscr-featured.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/4/47/Sound-icon.svg/20px-Sound-icon.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Ambox_current_red_Asia_Australia.svg/42px-Ambox_current_red_Asia_Australia.svg.png"}

        loc = 0
        while allImagesOnPage[loc]['src'] in ignore:
            loc = loc + 1

        requestedImage = allImagesOnPage[loc]['src']
        # # gets the src of each image
        print(requestedImage)

        requestedImage = "https:" + requestedImage.replace(
            requestedImage[requestedImage.find("px") - 3:requestedImage.find("px")], "1000")
        # remakes the links so the image is 1000px high
        print(requestedImage)

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

# def main():
#     currDate = datetime.now()
#     month = currDate.strftime("%B")
#     currDay = currDate.day
#
#     t = ImageDownload(wikipedia.page(month + " " + str(currDay)).html())
#     x = t.download(61)
#     # t.deleteImage(x)
#
#
# #     # l = []
# #     # for i in range(40):
# #     #     print("TIMES: " + str(i))
# #     #     l.append(t.download(i))
# #     #
# #     # time.sleep(10)
# #     #
# #     # for k in range(len(l)):
# #     #     if l[k]:
# #     #         t.deleteImage(l[k])
# #
# #
# if __name__ == '__main__':
#     main()
