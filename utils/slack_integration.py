from slack import WebClient
from slack.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()

# Slack Integration - Will send us messages (its optional)
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
client = WebClient(
    token=SLACK_TOKEN)


def post_slack_message(text, id):
    try:
        client.chat_postMessage(
            channel='#twitter-updates', text=text)
    except:
        pass