import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import auth_keys as keys
import json

class StdOutListener(StreamListener):
    def on_data(self, data):
        d = json.loads(data)
        for k in d:
            print(k, ":", d[k])
        #sys.exit()
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    listener = StdOutListener()
    auth = OAuthHandler(keys.CONSUMER_API_KEY, keys.CONSUMER_API_SECRET_KEY)
    auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    keywords = [
        "Donald Trump"
    ]
    stream.filter(track=keywords)
