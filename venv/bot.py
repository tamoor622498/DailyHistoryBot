import wikipedia
import datetime
import time
import tweepy
import random
import authentication #Holds twitter log in data.

api = authentication.authFunc() #Returns the API object

# Create a tweet
mydate = datetime.datetime.now()
s = mydate.strftime("%B")
s = s + " " + str(mydate.day)
t = wikipedia.page(s)
x = t.section("Events")
f = x.splitlines()

print("TTTTTTTTTT")

#api.update_status("Git Test.")

# for x in range(0,4):
#     loc = random.randrange(0,len(f))
#     out = "Today in " + f[loc]
#     f.pop(loc)
#     #api.update_status(out)
#     time.sleep(60)