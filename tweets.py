import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API
import auth_keys as keys
import json
import time
import re
from profanity_check import predict, predict_prob

"""
USEFUL KEYS
key                 : example
"created_at"        : Mon Jun 08 16:03:49 +0000 2020
"text"              : RT @_veevyan: hey guys. I promise …
"retweeted_status"  : dict of retweet info if retweet
    "quoted_status"     : dict of quote status if quote
    "extended_tweet" "full_text"    : full tweet
"""

def display_data(data):
    for key in data:
        print(key, ":", data[key])

class StdOutListener(StreamListener):
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def on_data(self, data):
        data_ = json.loads(data)
        name = data_["user"]["name"]
        handle = data_["user"]["screen_name"]
        authors = f"{name} (@{handle})"
        if "extended_tweet" in data_:
            tweet = data_["extended_tweet"]["full_text"]
        elif "retweeted_status" in data_:
            return
            if "extended_tweet" in data_["retweeted_status"]:
                tweet = data_["retweeted_status"]["extended_tweet"]["full_text"]
            else:
                tweet = data_["retweeted_status"]["text"]
            rt_name = data_["retweeted_status"]["user"]["name"]
            rt_handle = data_["retweeted_status"]["user"]["screen_name"]
            authors += f" RT {rt_name} (@{rt_handle})"
        else:
            tweet = data_["text"]

        if "quoted_status" in data_:
            return
            if "extended_tweet" in data_["quoted_status"]:
                quote = data_["quoted_status"]["extended_tweet"]["full_text"]
            else:
                quote = data_["quoted_status"]["text"]
            q_name = data_["quoted_status"]["user"]["name"]
            q_handle = data_["quoted_status"]["user"]["screen_name"]
            tweet = tweet + f"\nQuoting {q_name} (@{q_handle})" + quote

        authors += ":"
        if predict([self.clean_tweet(tweet)])[0]:
            print(authors)
            print(tweet)
            print("-----------------------------------")
            file.write(authors + "\n")
            file.write(tweet + "\n")
            file.write("----------------------------------------------------\n")
        return True

    def on_error(self, status):
        print(status)

    def on_exception(self, exception):
        print(exception)
        return

if __name__ == "__main__":

    listener = StdOutListener()
    auth = OAuthHandler(keys.CONSUMER_API_KEY, keys.CONSUMER_API_SECRET_KEY)
    auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
    api = API(auth_handler=auth)
    stream = Stream(auth, listener)

    keywords = [
        "Donald Trump"
    ]
    with open('tweets_test.txt', 'w', encoding='utf-8') as file:
        stream.filter(track=keywords)

    #print(api.get_status("125657359841361920"))
    # the_d = api.get_user("realDonaldTrump")
    # the_d = api.user_timeline("25073877", tweet_mode="extended")
    # for item in the_d:
    #     if "retweeted_status" in item._json:
    #         if "extended_tweet" in item._json["retweeted_status"]:
    #             tweet = item._json["retweeted_status"]["extended_tweet"]["full_text"]
    #         else:
    #             tweet = item._json["retweeted_status"]["full_text"]
    #     else:
    #         tweet = item._json["full_text"]
    #     print(tweet)
    #     print("------------------------------------------")
    #print(api.search("donald trump"))

    # print(api.trends_available())
    # with open('trending.txt', 'w', encoding='utf-8') as file:
    #     # 1 : worldwide
    #     # 23424975 : UK
    #     # 26062 : Leicester
    #     # 26734 : Liverpool
    #     for item in api.trends_place(23424975)[0]["trends"]:   # arg is a Yahoo! Where On Earth ID
    #         print(item['name'], ":", item['tweet_volume'])
    #         file.write(item['name'] + " : " + str(item['tweet_volume']) + "\n")
