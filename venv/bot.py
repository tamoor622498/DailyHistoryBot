import wikipedia
from datetime import datetime
import time
import tweepy
import random

import authentication  # Holds twitter log in data.

# global variables
api = authentication.authFunc()  # Returns the API object


def getEvents(day):  # Gets the array of events for given day
    events = wikipedia.page(day)
    events = events.section("Events")
    events = events.splitlines()
    return events


def daySetUp():
    global mydate
    global month
    global currentDay
    global monthAndDay

    mydate = datetime.now()
    month = mydate.strftime("%B")
    currentDay = mydate.day
    monthAndDay = month + " " + str(currentDay)


def main():
    daySetUp()

    events = getEvents(monthAndDay)
    while (currentDay == mydate.day):
        now = datetime.now().time()
        loc = random.randrange(0, len(events))
        out = monthAndDay + " " + events[loc]
        events.pop(loc)
        print(out, "tweeted at ", now)
        api.update_status(out)
        time.sleep(3600)


if __name__ == '__main__':
    main()
