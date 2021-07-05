[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


# DailyHistoryBot 2.0
A python twitter bot that posts history facts related to the day from Wikipedia with related images. This is meant to function using python3.

### Main Libraries:
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Scrapes webpages and parces the HTML to get the daily event data and images.

* [tweepy](https://pypi.org/project/tweepy/) - Tweets to a twitter account using python code.

* [lxml](https://pypi.org/project/lxml/) - Parcer used for BeautifulSoup.

* [requests](https://pypi.org/project/requests/) - Grabs page HTML and downloads images.

### Authentication.py:
>import tweepy  
>def authFunc():  
>    auth = tweepy.OAuthHandler("CONSUMER_KEY","CONSUMER_SECRET")  
>    auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")  
>    return tweepy.API(auth)  

The file or function should look like this. I have not included then in the repo for the security of my twitter account.  
You can get the keys and tokens by signing up for a twitter developer account. For detailed tutorial, look at this [guide](https://realpython.com/twitter-bot-python-tweepy/).