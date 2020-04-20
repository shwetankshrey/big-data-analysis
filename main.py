import tweepy

class ReservoirSamplingStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

CONSUMER_KEY = "XXXXXXXXX"
CONSUMER_SECRET = "XXXXXXXXX"
ACCESS_TOKEN = "XXXXXXXXX"
ACCESS_TOKEN_SECRET = "XXXXXXXXX"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

stream_listener = ReservoirSamplingStreamListener()
stream = tweepy.Stream(auth = api.auth, listener=stream_listener)

corona_hashtags = ['#Covid19', '#Coronavirus']
stream.filter(track=corona_hashtags, is_async=True)