from bs4 import BeautifulSoup
import os
import re
from datetime import datetime  # Used for getting current date
import requests
import wikipedia
import time
import tweepy  # Twitter API
import random

import realAuthentication
# Holds twitter login data.

api = realAuthentication.authFunc()
# Returns the API object

class Events:
    def __init__(self):
        self.getEvents()

    def getEvents(self):
        self.saveFolder = "MEDIA"
        self.fileName = "tweetImage"

        self.currDate = datetime.now() #Current time and date
        self.month = self.currDate.strftime("%B") #Gets month in str
        self.day = self.currDate.day #day in int
        self.monthAndDay = self.month + "_" + str(self.day) #Month and date combined into single month and day str

        self.wikiLink = "https://en.wikipedia.org/wiki/"+self.monthAndDay #Wikipage link made
        page = requests.get(self.wikiLink) #Site gotten
        
        pageSoup = BeautifulSoup(page.text, 'lxml') #Inputs HTML and sets up parcer
        eventsSection = pageSoup.find_all("h2")[1] #"Events" section is always the second h2 tag
        self.allEvents = list() #Holds li tag for each event of the day
        for tag in eventsSection.find_next_siblings(): #Loops through tags same height as h2
            if (tag.name == "ul"):
                self.allEvents.extend(tag.find_all("li")) #Adds the event li's to full list

            if (tag.name == "h2"): #Goes till the next h2 tag, "Births" section
                break

        for event in self.allEvents: #Go through each event
            children = event.findChildren() #Get all sub tags
            for child in children: #Loops through the sub tags
                if child.name == "sup": #If "sup" tag, remove from li
                    child.decompose()

    def eventsPrinter(self):
        eventIndex = random.randrange(0, len(self.allEvents))
        event = self.allEvents[eventIndex]
        output = self.monthAndDay.replace("_", " ") + ", " + event.getText().replace("   ", " ") + " #TodayInHistory"
        
        print("OUTPUT IS: "+output)

        potentialLinks = event.findChildren('a')
        if ((potentialLinks[0].getText().isnumeric()) or ("BC" in potentialLinks[0].getText()) or (("AD" in potentialLinks[0].getText()))):
            potentialLinks.pop(0)

        gotImage = False
        
        for link in potentialLinks:
            print("Getting image for: " + link.getText())
            gotImage = self.downloadImage(link['href'].replace("/wiki/", ""))
            if (gotImage):
                break

        wait = True

        if (gotImage):
            try:
                media_list = []
                response = api.media_upload(self.imageLoc)
                media_list.append(response.media_id_string)
                api.update_status(output, media_ids=media_list)
                print("Image was tweeted.")
                #tweets with image
            except tweepy.error.TweepError as e:
                wait = False
                if e.api_code == 182:
                    print("Repeat Tweet: "+ output)
                elif e.api_code == 186:
                    print("Tweet too long: "+ output)
                else:
                    print("Not tweeted: "+ str(e.api_code)+"-"+e.reason)

        else:
            try:
                api.update_status(output)
                print("Image was not tweeted")
            except tweepy.error.TweepError as e:
                wait = False
                if e.api_code == 182:
                    print("Repeat Tweet: "+ output)
                elif e.api_code == 186:
                    print("Tweet too long: "+ output)
                else:
                    print("Not tweeted: "+ str(e.api_code)+"-"+e.reason)

        self.allEvents.pop(eventIndex)

        try:
            self.deleteImage()
            # Deletes downloaded image
        except:
            pass

        if (wait):
            print(output, " tweeted at ", datetime.now().time())
            time.sleep(3600 * 2)

        self.dayChange()

        
        


    def downloadImage(self, page):
        if not os.path.exists(self.saveFolder): #Creates folder if it's not there
            os.mkdir(self.saveFolder)

        wikiPage = requests.get("https://en.wikipedia.org/wiki/"+page)
        imageSoup = BeautifulSoup(wikiPage.text, 'html.parser')
        
        img_tags = imageSoup.find_all('img')

        if (len(img_tags) < 1):
            return False


        ignore = {"//upload.wikimedia.org/wikipedia/en/thumb/9/99/Question_book-new.svg/50px-Question_book-new.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/9/94/Symbol_support_vote.svg/19px-Symbol_support_vote.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Text_document_with_red_question_mark.svg/40px-Text_document_with_red_question_mark.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/b/b4/Ambox_important.svg/40px-Ambox_important.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Crystal_Clear_app_kedit.svg/40px-Crystal_Clear_app_kedit.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/e/e7/Cscr-featured.svg/20px-Cscr-featured.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/4/47/Sound-icon.svg/20px-Sound-icon.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Ambox_current_red_Asia_Australia.svg/42px-Ambox_current_red_Asia_Australia.svg.png",
                  "/static/images/footer/wikimedia-button.png",
                  "/static/images/footer/poweredby_mediawiki_88x31.png",
                  "//en.wikipedia.org/wiki/Special:CentralAutoLogin/start?type=1x1",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Red_pog.svg/8px-Red_pog.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/9/94/Symbol_support_vote.svg/19px-Symbol_support_vote.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/8/8a/OOjs_UI_icon_edit-ltr-progressive.svg/10px-OOjs_UI_icon_edit-ltr-progressive.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/4/4a/Commons-logo.svg/12px-Commons-logo.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/4/48/Black_and_white_camera_icon.svg/25px-Black_and_white_camera_icon.svg.png",
                  "//upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/30px-Flag_of_the_United_States.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Translation_to_english_arrow.svg/50px-Translation_to_english_arrow.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/7/74/Red_Pencil_Icon.png"}

        imageLink = None
        for img in img_tags:
            if (img['src'] not in ignore and (int(re.findall(r"(\d+)px", img['src'])[0]) > 99)):
                imageLink = img['src']
                break

        if (imageLink == None):
            return False
        
        print(imageLink)

        image = requests.get("https:"+imageLink)
        fileExtension = imageLink[len(imageLink) - 4:len(imageLink)]

        self.imageName = "tweetImage" + fileExtension

        self.imageLoc = self.saveFolder + '/' + self.imageName

        with open(self.imageLoc, 'wb') as file:
            file.write(image.content)
        
        return True

    def deleteImage(self):
        if self.imageLoc:
            print("DELETING: " + self.imageLoc)
            os.remove(self.imageLoc)

    def dayChange(self):
        if (len(self.allEvents) < 0):
            while self.day == datetime.now().day:
                time.sleep(60)


def main():
    eventsBot = Events()
    eventsBot.eventsPrinter()


if __name__ == '__main__':
    main()
