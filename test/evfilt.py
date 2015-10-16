class Event(object):

    __init__(self):
        self.feed_objects = tweepy.Cursor(
                    twitter.list_timeline,list_id=211679718,
                    include_rts=False
                )
        self.time_objects = []

    def sample_ev(self, event):
        """Sample tweets within 2 hours of given time and date (format HH:MM MM-DD-YY)."""
        event_utc = (
                datetime.strptime(event, '%b %d %Y %H:%M:%S') +
                timedelta(hours=5)
            )
        event_format = event_utc.strftime('%b %d %H:%M:%S') # only for cdt atm
        cutoff = (
                event_utc + timedelta(hours=2)
            ).strftime('%b %d %H:%M:%S')
        print cutoff
        print event_format
        for tweet in self.feed_objects.items(9999):
            data = tweet._json
            raw_time = datetime.strptime(
                        data['created_at'],
                        '%a %b %d %H:%M:%S +0000 %Y'
                    )
            time = raw_time.strftime('%b %d %H:%M:%S')
            count = 0
            if time > cutoff: # have yet to get this to work
                pass
            else:
                if time > event_format:
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
            score = ((1.5*data['retweet_count'] + data['favorite_count'])
                     / (data['user']['followers_count'] / 2))*1000
            scores[round(score, 2)] = u"{0} at {1}: {2}".format(
                        data['user']['screen_name'], data['created_at'],
                        tweet.text
                    )
        pprint(sorted(scores.items(), reverse=True)[:10])
        scores.clear()

    def rank_ev(self, event):
        """Rank tweets within two hours of given time, x."""
        self.sample.sample_ev(event)
        self.score(self.sample.time_objects)

go = Event()
go.rank_ev('sep 15 2015 16:00:00')
