import requests
from datetime import datetime, timedelta
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

class Sample(object):
    """For time-based queries, cull tweets within period or proximity of event."""

    def __init__(self, which):
        self.which = which
        self.feed_objects = tweepy.Cursor(
                    twitter.list_timeline,list_id=self.which,
                    include_rts=False
                )
        self.time_objects = []

    def sample_per(self, hours):
        """For time queries, pull tweets from defined period."""
        cutoff = (
                datetime.utcnow() - timedelta(hours=hours)
            ).strftime('%b %d %H:%M:%S')
        for tweet in self.feed_objects.items():
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

class Rank(object):
    """Score and rank tweets by volume or time period."""

    def __init__(self):
        list_names = {}
        list_ids = {}
        list_objects = twitter.lists_all(screen_name=me)
        key = 1
        for list_ in list_objects:
            list_names[key] = list_.name
            list_ids[key] = list_.id
            key += 1
        print "Found your lists!"
        pprint(list_names)
        which = list_ids[int(raw_input("""Which list?
> """))]
        self.sample = Sample(which)

    def score(self, objects):
        """For both time and volume queries, rank tweet sample according
        to formula equaling 1.5 times number of retweets plus
        number of favorites, all divided by half number of followers."""
        scores = {}
        for tweet in objects:
            data = tweet._json
            score = ((1.5*data['retweet_count'] + data['favorite_count'])
                     / (data['user']['followers_count'] / 1.5))*1000
            scores[round(score, 2)] = u"{0} at {1}: {2}".format(
                        data['user']['screen_name'], data['created_at'],
                        tweet.text
                    )
        pprint(sorted(scores.items(), reverse=True)[:10])
        scores.clear()

    def rank_vol(self, volume):
        """Rank most recent x tweets, where x = volume."""
        self.score(self.sample.feed_objects.items(volume))

    def rank_per(self, hours):
        """Rank tweets from last x hours, where x = events."""
        self.sample.sample_per(hours)
        self.score(self.sample.time_objects)
