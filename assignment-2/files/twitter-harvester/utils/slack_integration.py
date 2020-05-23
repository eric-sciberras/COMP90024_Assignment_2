import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Slack Integration - Will send us messages (its optional)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def post_slack_message(text, id):
    data = {
        'text': text,
        'username': f'Twitter Harvester {id}',
        'icon_emoji': ':robot_face:'
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=data, headers={
            'Content-Type': 'application/json'})
    except:
        pass
