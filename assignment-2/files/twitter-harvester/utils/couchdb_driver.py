from cloudant import CouchDB
from dotenv import load_dotenv
import json
import logging
import os

# load env vars from .env file
load_dotenv()

COUCH_URL = os.getenv("COUCHDB_URL")
USERNAME = os.getenv("COUCHDB_USERNAME")
PASSWORD = os.getenv("COUCHDB_PASSWORD")
DB_NAME = os.getenv("COUCHDB_DB_NAME")

couch = CouchDB(USERNAME,PASSWORD,url=COUCH_URL, connect=True, auto_renew=True)

couch.create_database(DB_NAME)
couch.create_database('twitter_harvester_checkpoint')
tweets_db = couch[DB_NAME]
harvester_checkpoint = couch['twitter_harvester_checkpoint']

def export_tweet(tweet):
    print(f'saving: {tweet["id_str"]}')
    tweet['_id'] = tweet['id_str']
    tweets_db.create_document(tweet)

def load_checkpoint(city):
    id = None
    try:
       id = harvester_checkpoint[city]['id']
    except KeyError:
        logging.info(f'No value for {city} found')
    except Exception as e:
        logging.error(f'{repr(e)}')
    logging.info(f'Value: {str(id)}')
    return id

def save_checkpoint(city, id):
    try:
        checkpoint = harvester_checkpoint[city]
    except KeyError:
        logging.info(f'No value for {city} found')
        harvester_checkpoint.create_document({"_id": city, "id":id })
    else:
        checkpoint['id'] = id
        checkpoint.save()
    return

# For testing locally
# import sys
# import json
# COUCH_URL = "172.26.133.168:5984"
# USERNAME = "admin"
# PASSWORD = "password"
# with open(sys.argv[1],'r') as f:
#     for (i,tweet) in enumerate(f.readlines()):
#         # print(i)
#         export_tweet(json.loads(tweet))