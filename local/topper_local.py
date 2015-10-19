#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
from time import mktime
from pprint import pprint
from math import log

import tweepy

from config import me, ckey, csecret

requests.packages.urllib3.disable_warnings()

OAUTH_KEYS = (
    ckey, csecret,
)
auth = tweepy.OAuthHandler(
    ckey, csecret
)
twitter = tweepy.API(auth,wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

class Rank(object):

    def __init__(self, which):
        self.feed_objects = tweepy.Cursor(
                    twitter.list_timeline,list_id=which,
                    include_rts=False,count=100
                )
        self.time_objects = []

    def sample_per(self, hours):
        """For time queries, pull tweets from defined period."""
        cutoff = (
                datetime.utcnow() - timedelta(hours=hours)
            ).strftime('%b %d %H:%M:%S')
        for tweet in self.feed_objects.items(99999):
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

    def score(self, objects):
        """For both time and volume queries, rank tweet sample according
        to formula equaling 1.5 times number of retweets plus
        number of favorites, all divided by half number of followers."""
        scores = {}
        for tweet in objects:
            data = tweet._json
            raw_time = datetime.strptime( # reformat created_at
                        data['created_at'],
                        '%a %b %d %H:%M:%S +0000 %Y'
                    )
            age = ((datetime.utcnow() - raw_time).seconds / 60) + 1
            followers = data['user']['followers_count']
            engagement = 1.25 * data['retweet_count'] + data['favorite_count']
            e2f = engagement / (followers*0.5) * 1000
            e2a =  engagement / (age*0.95) * 100
            score = e2f + e2a
            print "Engagement: {0}, Age: {1}, E2F: {2}, E2A: {3}".format(
                                                        engagement, age,
                                                        e2f, e2a
                                                    )
            scores[round(score, 2)] = u"{0} at {1}: {2}".format(
                        data['user']['screen_name'], data['created_at'],
                        tweet.text
                    )
        pprint(sorted(scores.items(), reverse=True)[:10])

    def rank_vol(self, volume):
        """Rank most recent x tweets, where x = volume."""
        self.score(self.feed_objects.items(volume))

    def rank_per(self, hours):
        """Rank tweets from last x hours, where x = events."""
        self.sample_per(hours)
        self.score(self.time_objects)

def get_lists():
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
    which = list_ids[int(raw_input("Which list? "))]
    return which
