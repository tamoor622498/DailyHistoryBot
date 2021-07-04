from bs4 import BeautifulSoup
from datetime import datetime  # Used for getting current date
import requests
import wikipedia
import time
import tweepy  # Twitter API
import random
from ImageDownload import ImageDownload  # Downloads images from twitter page.

import authentication
# Holds twitter login data.

api = authentication.authFunc()
# Returns the API object

class Events:
    def __init__(self):
        self.getEvents()

    def getEvents(self):
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
        event = self.allEvents[2]
        link = event.find_all('a', href=True)[2]['href'].replace("/wiki/","")

        print(wikipedia.WikipediaPage(link).images)
        print(wikipedia.WikipediaPage(link))
        # for link in event.find_all('a', href=True):
        #     print(link['href'])

        

        # while (True):
        #     now = datetime.now().time()
        #     # Current time

        #     loc = random.randrange(0, len(self.currDayEvents))
        #     while not self.currDayEvents[loc]:
        #         loc = random.randrange(0, len(self.currDayEvents))
        #     # So not the location isn't false
        #     # Random part in list

        #     output = self.monthAndDay + ", " + self.currDayEvents[loc] + " #TodayInHistory"
        #     # Adds date in front of event


        #     imgPath = self.downloader.download(loc)
        #     # Path to downloaded image

        #     self.currDayEvents[loc] = False
        #     # Set as used.
        #     # Not removed from list so not out of line with page

        #     try:
        #         if imgPath:
        #             try:
        #                 # print(output)
        #                 media_list = []
        #                 response = api.media_upload(imgPath)
        #                 media_list.append(response.media_id_string)
        #                 api.update_status(output, media_ids=media_list)
        #                 print("Image was tweeted.")
        #                 # This just tweets the image

        #             except:
        #                 # print(output)
        #                 #print("Image not tweeted.")
        #                 api.update_status(output)
        #                 # If image errors out
        #         else:
        #             # print(output)
        #             api.update_status(output)
        #             # No image path

        #         print(output, "tweeted at ", now)
        #         time.sleep(3600 * 2)

        #     except tweepy.error.TweepError as e:
        #         # gets error

        #         if e.api_code == 187:
        #             # 187 is repeated tweet error code
        #             print("Repeated Tweet: ", output)
        #         else:
        #             print("Exception: ", e.reason)
        #             # Any other reason

        #     try:
        #         self.downloader.deleteImage(imgPath)
        #         # Deletes downloaded image
        #     except:
        #         pass

        #     if len(self.currDayEvents) < 1:
        #         while self.currDay == datetime.now().day:
        #             time.sleep(10)
        #     # If the list of events is depleted, wait till next day.

        #     if self.currDay != datetime.now().day:
        #         self.updateDay()
        #         self.getEvents()
        #     # If day changes, reload


def main():
    eventsBot = Events()
    eventsBot.eventsPrinter()


if __name__ == '__main__':
    main()
