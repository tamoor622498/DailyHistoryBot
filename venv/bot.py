import wikipedia
from datetime import datetime
import time
import tweepy
import random

import authentication  # Holds twitter log in data.

api = authentication.authFunc()  # Returns the API object


def getEvents(day):  # Gets the array of events for given day
    events = wikipedia.page(day)#Wiki page for current day
    events = events.section("Events")#String of the entire Events section
    events = events.splitlines()#Turns string in to list of event strings
    return events


def daySetUp():
    global mydate
    global month
    global currentDay
    global monthAndDay

    mydate = datetime.now()#current date
    month = mydate.strftime("%B")#String of month name
    currentDay = mydate.day#Day int
    monthAndDay = month + " " + str(currentDay)


def main():
    daySetUp()
    events = getEvents(monthAndDay)

    while (currentDay == mydate.day):#Goes till day changes (RPi reboots at midnight to restart code)
        if (len(events) < 1):#All string values printed
            break
        now = datetime.now().time()#Current time
        loc = random.randrange(0, len(events))#Random part in list
        out = monthAndDay + " " + events[loc]#Adds date in front of event
        events.pop(loc)#Event removes from list
        try:
            api.update_status(out)
            print(out, "tweeted at ", now)
            time.sleep(3600)
        except tweepy.error.TweepError as e:
            if (e.api_code == 187):#If tweet repeated
                print("Repeated Tweet: ", out)
            else:
                print("Exception: ", e.reason)#Anyother reason


if __name__ == '__main__':
    main()
