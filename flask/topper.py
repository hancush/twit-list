from datetime import datetime, timedelta

import tweepy

from config import ckey, csecret

auth = tweepy.OAuthHandler(ckey, csecret)
twitter = tweepy.API(auth)

def get_lists(user):
    """Populate dropdown with lists for given user."""
    list_options = {}
    list_objects = twitter.lists_all(screen_name=user)
    for list_ in list_objects:
        list_options[list_.id] = list_.name
    return list_options.items()

def get_tweets(which, hours):
    """Sample tweets from given list within given time period."""
    objects = tweepy.Cursor(
                twitter.list_timeline,list_id=which,
                include_rts=False,count=100
            ).items()
    time_objects = []
    cutoff = (
            datetime.utcnow() - timedelta(hours=hours)
        ).strftime('%b %d %H:%M:%S')
    for tweet in objects:
        data = tweet._json # isolate metadata
        raw_time = datetime.strptime(
                    data['created_at'],
                    '%a %b %d %H:%M:%S +0000 %Y'
                )
        time = raw_time.strftime('%b %d %H:%M:%S') # reformat to match cutoff for boolean
        if time > cutoff:
            time_objects.append(tweet)
    return time_objects

def score_tweets(objects):
    """Rank tweet sample according to ratio of engagement to followers.
    Retweets are weighted 1.5, followers are halved to reduce unfair
    advtantage to accounts with smaller followings."""
    scores = {}
    for tweet in objects:
        data = tweet._json
        rt = data['retweet_count']
        fave = data['favorite_count']
        fol = data['user']['followers_count']
        weight = 1.5
        score = ((weight * rt + fave) / (fol / 2)) * 1000
        scores[score] = data['id']
    embeds = []
    for item in sorted(scores.items(), reverse=True)[:13]: #sorted returns tuple
        embed = twitter.get_oembed(id=item[1],align='center')
        embeds.append(embed['html'])
    return embeds

################
##  testing   ##
################

def alt_score(objects):
    """In larger samples, older tweets have a slight advantage. Is
    there a way to incorporate age into score bearing in mind that tweets
    receive most engagement directly proximate to the time they are
    posted?"""
    scores = {}
    for tweet in objects:
        data = tweet._json
        raw_time = datetime.strptime(
                    data['created_at'],
                    '%a %b %d %H:%M:%S +0000 %Y'
                )
        age = ((datetime.utcnow() - raw_time).seconds / 60) + 1
        rt = data['retweet_count']
        fave = data['favorite_count']
        fol = data['user']['followers_count']
        weight = 1.5
        e2f = ((weight * rt + fave) / (fol / 2)) * 1000
        e2a =  enagement / age
        score = e2f + e2a
        scores[score] = data['id']
    embeds = []
    for item in sorted(scores.items(), reverse=True)[:13]:
        embed = twitter.get_oembed(id=item[1], align='center')
        embeds.append(embed['html'])
    return embeds
