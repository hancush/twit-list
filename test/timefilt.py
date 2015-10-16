from datetime import datetime, timedelta
import tweepy
from pprint import pprint
from config import *
import requests
requests.packages.urllib3.disable_warnings()

OAUTH_KEYS = (ckey, csecret, atoken, asecret)
auth = tweepy.OAuthHandler(ckey, csecret)
twitter = tweepy.API(auth)

timeline = tweepy.Cursor(twitter.list_timeline, list_id=211679718).items(999)

count = 0
tweets = []
tweet_scores = {}
now = datetime.now().strftime('%H:%M:%S')
cutoff = (datetime.now() - timedelta(hours=1)).strftime('%H:%M:%S')

for tweet in timeline:
    count += 1
    data = tweet._json
    # format created_at string to datetime #
    raw_time = datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    # convert created_at from UTC to CDT (my local time) #
    adjust_time = raw_time - timedelta(hours=5)
    # reformat adjusted time to hour:minute:second as string #
    time = adjust_time.strftime('%H:%M:%S')
    if time > cutoff:
        tweets.append(tweet)
    else:
        print count, time, tweet.text, time > cutoff
        break

def rank_tweets(x):
    for tweet in x:
        data = tweet._json
        text = u"{0} at {1}: \"{2}\"".format(
            data['user']['screen_name'],
            (datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y') - timedelta(hours=5)),
            tweet.text
        ) # u = unicode; default ascii encoding can't handle emoji
        score = (1.5*data['retweet_count'] + data['favorite_count'])
        tweet_scores[score] = text

print "Now: ", now
print "Cutoff ", cutoff

rank_tweets(tweets)

pprint(sorted(tweet_scores.items(), reverse=True)[:10])
