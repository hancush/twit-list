import tweepy
import time

ckey = "xjOxpfYcnUwpHabLXigPf3qrq"
csecret = "Dwv4mf6VqdUxtaPOWzoBIfSmXUXFXsfXqxKtLx4dxFNL684seQ"
atoken = "15817979-PGh6OVn1MI2vNC1M67lk6yNIEDMF7zFRyZ12tfXhq"
asecret = "0riruFEBY1kHJIC5wuRtzGatAgm57F1NGd4kvJvCrbxKc"

OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,
    'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)

import codecs
fp = codecs.open("Tweets.txt", "w", "utf-8")

# Extract the first "xxx" tweets related to "fast car"
counter = 0
for tweet in tweepy.Cursor(api.search, q='debate', since='2015-08-06', until='2015-08-07').items(3201): # need to figure out how to extract all tweets in the previous day
   # if tweet.geo != None:
  # print "Fetching tweet %s" % 
   # print "Tweet created:", tweet.created_at
   fp.write("%s\n" % unicode(tweet.text)) 
   counter += 1
   print counter

    #print ""
print "Captured %s tweets" % counter