# ranks last 5 tweets from each member of list, or last 500 tweets in list timeline
# returns top 10 tweets with most retweets/favorites (RTs weighted 50%)

from twython import Twython
from config import *
import pprint
import requests
requests.packages.urllib3.disable_warnings()

APP_KEY = ckey
APP_SECRET = csecret
OAUTH_TOKEN = atoken
OAUTH_TOKEN_SECRET = asecret

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

list_names = {}
list_ids = {}
members = []
tweet_scores = {} # need to look into alternate data structures that can tie score to tweet

def get_lists():
    list_objects = twitter.show_lists()
    key = 1
    for list in list_objects:
        list_names[key] = list['name']
        list_ids[key] = list['id']
        key += 1
    print "Found your lists!"
    pprint.pprint(list_names)

def rank_tweets(x):
    for tweet in x:
        text = tweet['user']['screen_name'] + ": \"" + tweet['text'] + "\""#, "created", tweet['created_at']
        score = (1.5*tweet['retweet_count'] + tweet['favorite_count'])
        tweet_scores[score] = text

def rank_member_tweets():
    member_objects = twitter.cursor(twitter.get_list_members, list_id=which) # get all user objects of list members
    for user in member_objects:
        members.append(user['screen_name']) # extact screen_name from each user object, add to list
    for user in members:
        tweet_objects = twitter.get_user_timeline(screen_name=user, count=5) # retrieve last 5 tweets from each user
        rank_tweets(tweet_objects) # feed tweets into ranking function
    pprint.pprint(sorted(tweet_scores.items(), reverse=True)[:10]) # display top 10 scoring tweets

def rank_timeline_tweets():
    tweet_objects = twitter.get_list_statuses(list_id=which,count=500) # get last 500 tweet objects from list feed
    rank_tweets(tweet_objects) # feed tweets into ranking function
    pprint.pprint(sorted(tweet_scores.items(), reverse=True)[:10]) # return top 10 scoring tweets

get_lists()

which = list_ids[int(raw_input("""Which list?
> """))]

print """
#Would you like to rank:

1: Last five tweets from each list member?
2: Last 200 tweets in list timeline?"
"""

answer = int(raw_input("> "))
if answer == 1:
    rank_member_tweets()
else:
    rank_timeline_tweets()
