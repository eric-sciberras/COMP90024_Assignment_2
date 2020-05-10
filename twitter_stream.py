'''
STILL NOT FULLY IMPLEMENTED.
Doesn't grab tweets over seperate states
but instead tweets matching a tag
'''

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

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)

# Our modules
import utils.twitter_filters as twitter_filters
from utils.process_tweets import process_tweets
from utils.slack_integration import post_slack_message
import utils.file_driver as file_driver
import utils.couchdb_driver as couchdb_driver

# load env vars from .env file
load_dotenv()

# Twitter Auth

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

harvester_id = sys.argv[0]


class Listener(StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener, self).__init__()
        self.output_file = output_file
        self.counter = 0

    # This function handles what we do with an incoming tweet
    def on_status(self, status):
        processed_tweet = process_tweets(status, "city")
        file_driver.export_tweets(processed_tweet)

        self.counter += 1
        if self.counter % 1000 == 0:
            post_slack_message(
                f"We now have {self.counter} Tweets.", harvester_id)

    def on_error(self, status_code):
        post_slack_message(
            f"Twitter is onto us ABORT ABORT.\n The status code given was {status_code}.", harvester_id)
        print(status_code)
        return False


tags = ['#jobseeker', '#jobkeeper']
# tags = ['#jobseeker', '#jobkeeper', '#job-seeker', '#job-keeper',
#         'jobseeker', 'jobkeeper', 'job-seeker', 'job-keeper', 'job seeker', 'job keeper']
australia_bounding_box = [113.338953078, -
                          43.6345972634, 153.569469029, -10.6681857235]
print('Start streaming.')
post_slack_message(f"We are up and running!!!",harvester_id)
output = open('jobseeker-jobkeeper.txt', 'a')
listener = Listener(output_file=output)

try:
    stream = Stream(auth=api.auth, listener=listener)
    stream.filter(languages=['en'], track=tags)
except KeyboardInterrupt:
    print('Stopping')
finally:
    post_slack_message(f"Restart me.",harvester_id)
    stream.disconnect()
    output.close()
