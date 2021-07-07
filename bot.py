from bs4 import BeautifulSoup
import os
import re
from datetime import datetime  # Used for getting current date
import requests
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
        while(True):
            self.dayChange() #Running out of events or day changed

            eventIndex = random.randrange(0, len(self.allEvents)) #Random index
            event = self.allEvents[eventIndex]
            output = self.monthAndDay.replace("_", " ") + ", " + event.getText().replace("   ", " ") + " #TodayInHistory" #Tweet formatted and formed
            
            print("OUTPUT IS: "+output)

            potentialLinks = event.findChildren('a') #Links to pages mentioned
            if ((potentialLinks[0].getText().isnumeric()) or ("BC" in potentialLinks[0].getText()) or (("AD" in potentialLinks[0].getText()))): #Removes the link for year
                potentialLinks.pop(0)

            gotImage = False #If an image was found
            
            for link in potentialLinks: #Loop through links till an image is downloaded
                print("Getting image for: " + link.getText())
                gotImage = self.downloadImage(link['href'].replace("/wiki/", "")) #True if image was saved
                if (gotImage):
                    break

            wait = True #Handle events that aren't able to be tweeted

            if (gotImage): #If image downloaded
                try:
                    media_list = []
                    response = api.media_upload(self.imageLoc) #Upload content
                    media_list.append(response.media_id_string)
                    api.update_status(output, media_ids=media_list) #Tweet with content
                    print("Image was tweeted.")
                    #tweets with image
                except tweepy.error.TweepError as e:
                    wait = False #Tweet failed, so don't wait to tweet next one
                    if e.api_code == 182:
                        print("Repeat Tweet: "+ output)
                    elif e.api_code == 186:
                        print("Tweet too long: "+ output)
                    else:
                        print("Not tweeted: "+ str(e.api_code)+"-"+e.reason)
            else: #No image gotten
                try:
                    api.update_status(output) #tweet just text
                    print("Image was not tweeted")
                except tweepy.error.TweepError as e:
                    wait = False #Tweet failed, so don't wait to tweet next one
                    if e.api_code == 182:
                        print("Repeat Tweet: "+ output)
                    elif e.api_code == 186:
                        print("Tweet too long: "+ output)
                    else:
                        print("Not tweeted: "+ str(e.api_code)+"-"+e.reason)

            self.allEvents.pop(eventIndex) #Remove event from list

            try:
                self.deleteImage() #Image clean up
                # Deletes downloaded image
            except:
                pass

            if (wait):
                print(output, " tweeted at ", datetime.now().time())
                time.sleep(3600 * 2) #Wait 2 hours for next tweet

    def downloadImage(self, page):
        if not os.path.exists(self.saveFolder): #Creates folder if it's not there
            os.mkdir(self.saveFolder)

        wikiPage = requests.get("https://en.wikipedia.org/wiki/"+page) #Get the page HTML
        imageSoup = BeautifulSoup(wikiPage.text, 'html.parser') #Load into BeautifulSoup
        
        img_tags = imageSoup.find_all('img') #Get's all images on the page

        if (len(img_tags) < 1): #If no images
            return False

        for img in img_tags:
            print(re.findall(r"(\d+)px", img['src']))

        # Internal WIKI images
        ignore = {"/static/images/footer/wikimedia-button.png",
                  "/static/images/footer/poweredby_mediawiki_88x31.png",
                  "//en.wikipedia.org/wiki/Special:CentralAutoLogin/start?type=1x1",
                  "//upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Red_pog.svg/8px-Red_pog.svg.png",
                  "//upload.wikimedia.org/wikipedia/commons/7/74/Red_Pencil_Icon.png"}

        imageLink = None #Tells if image is found
        for img in img_tags:
            regArray = re.findall(r"(\d+)px", img['src'])
            if (len(regArray) > 0):
                if (img['src'] not in ignore and (int(regArray[0]) > 99)): #If link not in ignore array and size greater that 99 pixels
                    imageLink = img['src']
                    break
            

        if (imageLink == None): #No image found
            return False
        
        print(imageLink)

        image = requests.get("https:"+imageLink) #Get the image page
        fileExtension = imageLink[len(imageLink) - 4:len(imageLink)] #Image format from link

        self.imageName = "tweetImage" + fileExtension 

        self.imageLoc = self.saveFolder + '/' + self.imageName #Image location

        with open(self.imageLoc, 'wb') as file: #Saving the image at location
            file.write(image.content)
        
        return True

    def deleteImage(self):
        if os.path.exists(self.imageLoc): #Delete if exsits
            print("DELETING: " + self.imageLoc)
            os.remove(self.imageLoc)

    def dayChange(self):
        if (len(self.allEvents) < 0): #If events run out
            while self.day == datetime.now().day:
                time.sleep(60)
        
        if self.day != datetime.now().day: #If day changes
                self.getEvents()


def main():
    eventsBot = Events()
    # eventsBot.eventsPrinter()

    eventsBot.downloadImage("1947_Sylhet_referendum")



if __name__ == '__main__':
    main()
