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

counter = 0
max_id = 0
harvester_id = sys.argv[0]
iterations_per_choice = 1
search_query = f"{' OR '.join(twitter_filters.tags)}"

post_slack_message(f"Starting Twitter Harvester: {harvester_id}", harvester_id)

'''
The Twitter havester works by grabbing the lastest tweets given by the /search endpoint. 
It works in 2 phases:

1.Grab all tweets newest to oldest (7 days old which is a limitation of the twitter API)
  This is done with the max_id attribtue. We do this for city major AUstralian city.

2.Grab the latest tweets but stop before we get to the tweets we have already collected.

We run phase 1 for each city, then move to phase 2
'''

while True:

    for city in twitter_filters.australian_city_geocodes:
        geocode = f'{city["latitude"]},{city["longitude"]},40km'
        max_id = file_driver.load_checkpoint(f'{city["name"]}_max_id')
        since_id = file_driver.load_checkpoint(f'{city["name"]}_since_id')

        for i in itertools.count():
            try:
                logging.info(f'calling twitter search api')
                tweets = api.search(q=search_query, lang="en", count=100, tweet_mode='extended',
                                    geocode=geocode, since_id=since_id, max_id=max_id, result_type='recent')
            except tweepy.TweepError as e:
                print(repr(e))
                post_slack_message(f"Twitter error: {repr(e)}", harvester_id)

            logging.info(
                f'we got {len(tweets)} tweets for state {city["name"]}')

            if tweets:
                # Process the tweets and then save them
                processed_tweets = process_tweets(
                    [tweet._json for tweet in tweets], city['name'])
                file_driver.export_tweets(processed_tweets)

                # House keeping
                counter += len(tweets)
                if counter % 1000 == 0:
                    post_slack_message(
                        f"We now have {counter} Tweets.", harvester_id)
                if (i == 0):
                    since_id_temp = tweets[0]._json['id']
                max_id = tweets[-1]._json['id'] - 1
                file_driver.save_checkpoint(f'{city["name"]}_max_id', max_id)
            else:
                print(f"No tweets {city['name']}")
                time.sleep(5)
                file_driver.save_checkpoint(
                        f'{city["name"]}_since_id', since_id_temp)
                file_driver.save_checkpoint(f'{city["name"]}_max_id', None)
                break
