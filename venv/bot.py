import wikipedia
import datetime
import time
import tweepy
import random
import authentication #Holds twitter log in data.

api = authentication.authFunc()  # Returns the API object

def main():

    # Create a tweet
    mydate = datetime.datetime.now()
    month = mydate.strftime("%B")
    monthAndDay = month + " " + str(mydate.day)
    wikiPage = wikipedia.page(monthAndDay)
    events = wikiPage.section("Events")
    events = events.splitlines()
    print(events[0])

if __name__ == '__main__':
    main()

#api.update_status("Hello World!")

# for x in range(0,4):
#     loc = random.randrange(0,len(f))
#     out = "Today in " + f[loc]
#     f.pop(loc)
#     #api.update_status(out)
#     time.sleep(60)