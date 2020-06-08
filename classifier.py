import re
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
import auth_keys as keys
from textblob import TextBlob
import time
import json
from gensim.parsing.preprocessing import remove_stopwords
import sys

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

class StreamToClassifier(StreamListener):
    def on_data(self, data):
        data_ = json.loads(data)
        if "extended_tweet" in data_:
            tweet = data_["extended_tweet"]["full_text"]
        elif "retweeted_status" in data_:
            return
            if "extended_tweet" in data_["retweeted_status"]:
                tweet = data_["retweeted_status"]["extended_tweet"]["full_text"]
            else:
                tweet = data_["retweeted_status"]["text"]
        else:
            tweet = data_["text"]
        #print(tweet)
        tweet = process_tweet(tweet)
        #print("----------")
        #print(tweet)
        analysis = get_tweet_sentiment(tweet)
        polarity = analysis.sentiment.polarity
        if polarity != 0:
            polarities.append(polarity)
        if polarity > 0:
            sentiment = "positive"
        elif polarity == 0:
            sentiment = "neutral"
        elif polarity < 0:
            sentiment = "negative"
        subjectivity = analysis.sentiment.subjectivity
        #print("polarity:", polarity, sentiment)
        #print("subjectivity:", analysis.sentiment.subjectivity)
        #print("--------------------------------------")
        restart_line()
        if not len(polarities):
            return True
        sys.stdout.write("average polarity:" + str(sum(polarities)/len(polarities)))
        sys.stdout.flush()
        return True

    def on_error(self, status):
        print(status)

    def on_exception(self, exception):
        print(exception)
        return

def process_tweet(tweet):
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        tweet = tweet.lower() # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', '', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = remove_stopwords(tweet)
        #tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        #tweet = remove_stopwords(tweet)
        return tweet

def get_tweet_sentiment(tweet):
        analysis = TextBlob(process_tweet(tweet))
        return analysis

if __name__ == "__main__":
    listener = StreamToClassifier()
    auth = OAuthHandler(keys.CONSUMER_API_KEY, keys.CONSUMER_API_SECRET_KEY)
    auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    keywords = [
        "Donald Trump"
    ]
    polarities = []
    stream.filter(track=keywords)
