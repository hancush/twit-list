# cobbled together solution using last 5 tweets from each member of list
# returns top 10 tweets with most retweets/favorites (RTs weighted 50%)
# doesn't seem to be reply count in tweet objects??

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
    tweet_scores = {} # need to look into alternate data structures that can tie score to tweet
    for tweet in x:
        text = tweet['user']['screen_name'] + ": \"" + tweet['text'] + "\""#, "created", tweet['created_at']
        score = (1.5*tweet['retweet_count'] + tweet['favorite_count'])
        tweet_scores[score] = text
    pprint.pprint(sorted(tweet_scores.items(), reverse=True)[:10])

def member_tweets():
    members = []
    member_objects = twitter.get_list_members(list_id=which)['users']
    for user in member_objects:
        members.append(user['screen_name'])
    for user in members:
        tweet_objects = twitter.get_user_timeline(screen_name=user,count=5,exclude_replies=True,include_rts=False)
        rank_tweets(tweet_objects)

def timeline_tweets():
    tweet_objects = twitter.get_list_statuses(list_id=which,count=200)
    rank_tweets(tweet_objects)

get_lists()

which = list_ids[int(raw_input("""Which list?
> """))]

print """
Would you like to rank:

1: Last five tweets from each list member?
2: Last 200 tweets from list?"
"""

answer = raw_input("> ")
if answer == 1:
    member_tweets()
else:
    timeline_tweets()
