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
        self.currDayEvents = wikipedia.page(self.monthAndDay).section("Events").splitlines()
        # This gets the Wikipedia page, then gets the "Events" section (returns block of text)
        # and uses .splitlines() to turn currDayEvents into a list.

    def eventsPrinter(self):
        while (True):
            now = datetime.now().time()
            # Current time
            loc = random.randrange(0, len(self.currDayEvents))
            # Random part in list
            output = self.monthAndDay + ", " + self.currDayEvents[loc] + " #TodayInHistory"
            # Adds date in front of event
            downloader = ImageDownload(self.month, self.currDay)
            imgPath = downloader.download(loc)
            # Path to downloaded image
            self.currDayEvents.pop(loc)
            # removed from list

            try:
                if imgPath:
                    try:
                        api.update_with_media(imgPath, output)
                        # Image found
                    except:
                        api.update_status(output)
                else:
                    api.update_status(output)
                    # No image path
                downloader.deleteImage(imgPath)
                # Downloaded image is deleted
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
