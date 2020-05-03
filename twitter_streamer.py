import sys
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import os
from slack import WebClient
from slack.errors import SlackApiError

from dotenv import load_dotenv
load_dotenv()

# Twitter keys
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)

# Slack Integration - Will send us messages (its optional)
SLACK_TOKEN = os.getenv("CONSUMER_SECRET")
client = WebClient(
    token=SLACK_TOKEN)

def post_slack_message(text):
    try:
        client.chat_postMessage(
            channel='#twitter-updates', text=text)
    except:
        pass

class Listener(StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener, self).__init__()
        self.output_file = output_file
        self.counter = 0

    # This function handles what we do with an incoming tweet
    def on_status(self, status):
        print(json.dumps(status._json), file=self.output_file)
        try:
            print(status.extended_tweet["full_text"])
        except AttributeError:
            print(status.text)
        self.counter += 1
        if self.counter % 1000 == 0 or self.counter == 10:
            post_slack_message(f"We now have {self.counter} Tweets.")
        print(f'{self.counter}', end='\r')

    def on_error(self, status_code):
        post_slack_message(
            f"Twitter is onto us ABORT ABORT.\n The status code given was {status_code}.")
        print(status_code)
        return False


tags = ['#jobseeker', '#jobkeeper']
# tags = ['#jobseeker', '#jobkeeper', '#job-seeker', '#job-keeper',
#         'jobseeker', 'jobkeeper', 'job-seeker', 'job-keeper']
australia_bounding_box = [113.338953078, -
                          43.6345972634, 153.569469029, -10.6681857235]
print('Start streaming.')
post_slack_message(f"We are up and running!!!")
output = open('stream_output_au.txt', 'a')
listener = Listener(output_file=output)

try:
    stream = Stream(auth=api.auth, listener=listener)
    stream.filter(languages=['en'], track=tags,
                  locations=australia_bounding_box)
except KeyboardInterrupt:
    print('Stopping')
finally:
    post_slack_message(f"Restart me.")
    stream.disconnect()
    output.close()

