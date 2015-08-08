import tweepy # must install tweepy locally (?)
import time # is anything using time here?

# create app at twitter dev to generate:
ckey = "xjOxpfYcnUwpHabLXigPf3qrq"
csecret = "Dwv4mf6VqdUxtaPOWzoBIfSmXUXFXsfXqxKtLx4dxFNL684seQ"
atoken = "15817979-PGh6OVn1MI2vNC1M67lk6yNIEDMF7zFRyZ12tfXhq"
asecret = "0riruFEBY1kHJIC5wuRtzGatAgm57F1NGd4kvJvCrbxKc"

# authorize with twitter api (for id purposes)
OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,
    'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)

import codecs
# create file object named fp by opening (or creating if dne) Tweets.txt in write mode with UTF-8 encoding
# temp workaround for emojis, which crash terminal if printed bc they contain backslash
fp = codecs.open("Tweets.txt", "w", "utf-8")

# write text of first .items(xxx) matching q='some query' to file
counter = 0 # set counter
for tweet in tweepy.Cursor(api.search, q='debate', since='2015-08-06', until='2015-08-07').items(3201): # need to figure out how to extract all tweets in the previous day
   # if tweet.geo != None:
   # print "Fetching tweet %s" %
   # print "Tweet created:", tweet.created_at
    fp.write("%s\n" % unicode(tweet.text)) # write status plus line break to fp
    counter += 1 # add one to counter each time tweet written to fp
    print counter # print counter as loop runs

print "Captured %s tweets" % counter # print final count when loop completed
