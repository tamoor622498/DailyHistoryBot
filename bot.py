import wikipedia  # Grabs events.
from datetime import datetime  # Used for getting current date
import time
import tweepy  # Twitter API
import random
from ImageDownload import ImageDownload  # Downloads images from twitter page.

import authentication

# Holds twitter log in data.

api = authentication.authFunc()


# Returns the API object

class Events:
    def __init__(self):
        self.updateDay()
        self.getEvents()

    def updateDay(self):
        self.currDate = datetime.now()
        self.month = self.currDate.strftime("%B")
        self.currDay = self.currDate.day
        self.monthAndDay = self.month + " " + str(self.currDay)

        # Sets up necessary data for query

    def getEvents(self):
        self.currDayEvents = wikipedia.page(self.monthAndDay, auto_suggest=False).section("Events").splitlines()

        self.downloader = ImageDownload(wikipedia.page(self.monthAndDay, auto_suggest=False).html())
        # This gets the Wikipedia page, then gets the "Events" section (returns block of text)
        # and uses .splitlines() to turn currDayEvents into a list.

    def eventsPrinter(self):
        while (True):
            now = datetime.now().time()
            # Current time

            loc = random.randrange(0, len(self.currDayEvents))
            while not self.currDayEvents[loc]:
                loc = random.randrange(0, len(self.currDayEvents))
            # So not the location isn't false
            # Random part in list

            output = self.monthAndDay + ", " + self.currDayEvents[loc] + " #TodayInHistory"
            # Adds date in front of event


            imgPath = self.downloader.download(loc)
            # Path to downloaded image

            self.currDayEvents[loc] = False
            # Set as used.
            # Not removed from list so not out of line with page

            try:
                if imgPath:
                    try:
                        # print(output)
                        media_list = []
                        response = api.media_upload(imgPath)
                        media_list.append(response.media_id_string)
                        api.update_status(output, media_ids=media_list)
                        print("Image was tweeted.")
                        # This just tweets the image

                    except:
                        # print(output)
                        #print("Image not tweeted.")
                        api.update_status(output)
                        # If image errors out
                else:
                    # print(output)
                    api.update_status(output)
                    # No image path

                print(output, "tweeted at ", now)
                time.sleep(3600 * 2)

            except tweepy.error.TweepError as e:
                # gets error

                if e.api_code == 187:
                    # 187 is repeated tweet error code
                    print("Repeated Tweet: ", output)
                else:
                    print("Exception: ", e.reason)
                    # Any other reason

            try:
                self.downloader.deleteImage(imgPath)
                # Deletes downloaded image
            except:
                pass

            if len(self.currDayEvents) < 1:
                while self.currDay == datetime.now().day:
                    time.sleep(10)
            # If the list of events is depleted, wait till next day.

            if self.currDay != datetime.now().day:
                self.updateDay()
                self.getEvents()
            # If day changes, reload


def main():
    eventsBot = Events()
    eventsBot.eventsPrinter()


if __name__ == '__main__':
    main()
