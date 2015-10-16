import requests
from datetime import datetime, timedelta
from pprint import pprint

import tweepy

from config import me, ckey, csecret

requests.packages.urllib3.disable_warnings()

OAUTH_KEYS = (
    ckey, csecret,
)
auth = tweepy.OAuthHandler(
    ckey, csecret
)
twitter = tweepy.API(auth)

class Rank(object):

    def __init__(self):
        pass

    def get_lists(self, user):
        """Get lists for given user."""
        list_options = {}
        list_objects = twitter.lists_all(screen_name=user)
        for list_ in list_objects:
            list_options[list_.id] = list_.name
        return list_options.items()

    def get_tweets(self, which):
        """Get tweets from given list."""
        return tweepy.Cursor(
                    twitter.list_timeline,list_id=which,
                    include_rts=False
                )

    def sample_per(self, objects, hours):
        """For time queries, pull tweets from defined period."""
        time_objects = []
        cutoff = (
                datetime.utcnow() - timedelta(hours=hours)
            ).strftime('%b %d %H:%M:%S')
        for tweet in objects.items(99999):
            data = tweet._json # isolate metadata
            raw_time = datetime.strptime( # reformat created_at
                        data['created_at'],
                        '%a %b %d %H:%M:%S +0000 %Y'
                    )
            time = raw_time.strftime('%b %d %H:%M:%S')
            if time > cutoff:
                time_objects.append(tweet)
            else:
                break
        return time_objects

    def score(self, objects):
        """For both time and volume queries, rank tweet sample according
        to formula equaling 1.5 times number of retweets plus
        number of favorites, all divided by half number of followers."""
        scores = {}
        for tweet in objects:
            data = tweet._json
            score = ((1.5*data['retweet_count'] + data['favorite_count'])
                     / (data['user']['followers_count'] / 1.5))*1000
            scores[round(score, 2)] = data['id']
        embeds = []
        for item in sorted(scores.items(), reverse=True)[:10]: #sorted returns tuple
            embed = twitter.get_oembed(id=item[1], align='center')
            embeds.append(embed['html'])
        return embeds

    def rank_vol(self, objects, volume):
        """Rank most recent x tweets, where x = volume."""
        self.score(objects.items(volume))

    #def rank_per(self, objects):
        #"""Rank tweets from last x hours, where x = events."""
        #self.score(time_objects)
