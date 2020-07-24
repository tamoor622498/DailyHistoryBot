[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


# DailyHistoryBot
A python twitter bot that posts history facts from Wikipedia and scrapes images.

### Need to pip install:
* [wikipediaAPI](https://pypi.org/project/wikipedia/) - Grabs the list of historical events for each day.

* [tweepy](https://pypi.org/project/tweepy/) - Tweets to a twitter account using python code.

* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Scrapes webpages and parces the HTML.

### Authentication.py:
>import tweepy  
>def authFunc():  
>    auth = tweepy.OAuthHandler("CONSUMER_KEY","CONSUMER_SECRET")  
>    auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")  
>    return tweepy.API(auth)  

The file or function should look like this. I have not included then in the repo for the security of my twitter account.  
You can get the keys and tokens by signing up for a twitter developer account. For detailed tutorial, look at this [guide](https://realpython.com/twitter-bot-python-tweepy/).

### Issues:
* The main issue is that some of the images "ImageDownload" gets are not tweetable using the API, but is able to be tweeted used the browser version. Another point of interest I've found is that this error is much more likely to occur on windows than on a linux distro. The latter leads me to conclude this is a problem with how windows saves images.