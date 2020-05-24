import wikipedia
from datetime import datetime
import time
import tweepy
import random

import authentication  # Holds twitter log in data.

api = authentication.authFunc()  # Returns the API object


class Events:
    def __init__(self):
        self.updateDay()
        self.getEvents()

    def updateDay(self):
        self.currDate = datetime.now()
        self.month = self.currDate.strftime("%B")
        self.currDay = self.currDate.day
        self.monthAndDay = self.month + " " + str(self.currDay)

    def getEvents(self):
        self.currDayEvents = wikipedia.page(self.monthAndDay).section("Events").splitlines()
        # This gets the wikipage, then gets the "Events" section (returns block of text)
        # and uses .splitlines() to turn currDayEvents into a list.

    def eventsPrinter(self):
        while (True):
            now = datetime.now().time()  # Current time
            loc = random.randrange(0, len(self.currDayEvents))  # Random part in list
            output = self.monthAndDay + " " + self.currDayEvents[loc] + " #TodayInHistory"  # Adds date in front of event
            self.currDayEvents.pop(loc)

            try:
                api.update_status(output)
                print(output, "tweeted at ", now)
                time.sleep(3600*2)
            except tweepy.error.TweepError as e:  # gets error
                if (e.api_code == 187):  # 187 is repeated tweet error code
                    print("Repeated Tweet: ", output)
                else:
                    print("Exception: ", e.reason)  # Any other reason

            if (len(self.currDayEvents) < 1):
                while(self.currDay == datetime.now().day):
                    time.sleep(10)

            if (self.currDay != datetime.now().day):#
                self.updateDay()
                self.getEvents()


def main():
    eventsBot = Events()
    eventsBot.eventsPrinter()


if __name__ == '__main__':
    main()
