import requests
from datetime import datetime
from datetime import timedelta
from pprint import pprint

import tweepy

from config import *

requests.packages.urllib3.disable_warnings()

OAUTH_KEYS = (
    ckey, csecret,
    atoken, asecret
)
auth = tweepy.OAuthHandler(
    ckey, csecret
)
twitter = tweepy.API(auth)

class Rank(object):
    """Score and rank tweets by volume or time period."""

    def __init__(self):
        self.feed_objects = tweepy.Cursor(
                    twitter.list_timeline,list_id=211679718,
                    include_rts=False
                )

    def sample(self, hours):
        """For time queries, pull tweets from defined period."""
        cutoff = (
                datetime.utcnow() - timedelta(hours=hours)
            ).strftime('%b %d %H:%M:%S')
        self.time_objects = []
        for tweet in self.feed_objects.items(9999):
            data = tweet._json # isolate metadata
            raw_time = datetime.strptime( # reformat created_at
                        data['created_at'],
                        '%a %b %d %H:%M:%S +0000 %Y'
                    )
            time = raw_time.strftime('%b %d %H:%M:%S')
            if time > cutoff:
                self.time_objects.append(tweet)
            else:
                break
        print cutoff

    def score(self, objects):
        """For both time and volume queries, rank tweet sample according
        to formula equaling 1.5 times number of retweets plus
        number of favorites, all divided by half number of followers."""
        scores = {}
        for tweet in objects:
            data = tweet._json # isolate metadata
            score = ((1.5*data['retweet_count'] + data['favorite_count'])
                     / (data['user']['followers_count'] / 2))*1000
            scores[round(score, 2)] = u"{0} at {1}: {2}".format(
                        data['user']['screen_name'], data['created_at'],
                        tweet.text
                    )
        pprint(sorted(scores.items(), reverse=True)[:10])
        scores.clear()

    def rank_vol(self, volume):
        """Sample number of tweets defined by volume argument."""
        self.score(self.feed_objects.items(volume))

    def rank_time(self, hours):
        """Sample tweets from time period defined by hours argument."""
        self.sample(hours)
        self.score(self.time_objects)
