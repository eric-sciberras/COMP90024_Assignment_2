
import sys
import tweepy
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import random
import logging
import itertools
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
import time

# Our modules
import utils.wait_for_connection as wait_for_connection
# Before we proceed wait for connection to the internet
wait_for_connection.wait()
import utils.twitter_filters as twitter_filters
from utils.process_tweets import process_tweet
from utils.slack_integration import post_slack_message
import utils.couchdb_driver as couchdb_driver

# load env vars from .env file
load_dotenv()

# Twitter Auth

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
HARVESTER_ID = os.getenv("HARVESTER_ID")
PING_EVERY_X_TWEETS = os.getenv("PING_EVERY_X_TWEETS")



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

post_slack_message(f"Starting Twitter Harvester: {HARVESTER_ID}", HARVESTER_ID)


class Listener(StreamListener):
    def __init__(self, run_time, city, tags):
        super(Listener, self).__init__()
        self.end_time = time.time() + run_time
        self.city = city
        self.counter = 0
        self.tags = tags

    # This function handles what we do with an incoming tweet
    def on_status(self, status):
        for tag in self.tags:
            if tag.lower() in (status.text).lower():
                print(f"found tag: {tag}")
                print(f"id: {status._json['id_str']}")
                processed_tweet = process_tweet(
                    status._json, self.city["name"])

                couchdb_driver.export_tweet(processed_tweet)

                self.counter += 1
                if self.counter % int(PING_EVERY_X_TWEETS) == 0:
                    post_slack_message(
                        f"We now have {self.counter} Tweets.", HARVESTER_ID)
                break

        if time.time() > self.end_time:
            print('Completed the Twitter data stream')
            return False

    def on_error(self, status_code):
        post_slack_message(
            f"The status code given was {status_code}.", HARVESTER_ID)


while True:
    try:
        # Pick a city
        city = random.choice(twitter_filters.australian_city_geocodes)
        print(f'{city["name"]} has been chosen')
        l = Listener(run_time=600,
                     city=city, tags=twitter_filters.tags)
        stream = Stream(auth=api.auth, listener=l, tweet_mode='extended')
        stream.filter(languages=['en'], locations=city['bounding_box'])
        break
    except Exception as e:
        print(repr(e))
        post_slack_message(f"Twitter error: {repr(e)}", HARVESTER_ID)
