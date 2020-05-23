# COMP90024_Assignment_2

## Folder Structure

``` shell
├── checkpoint.pickle
├── debug.json
├── example.env
├── README.md
├── twitter_search.py
├── twitter_stream.py
└── utils
    ├── couchdb_driver.py
    ├── file_driver.py
    ├── process_tweets.py
    ├── slack_integration.py
    └── twitter_filters.py
```

- *checkpoint.pickle*: Checkpoint file used to keep track of which tweets have been retrieved from the `twtter_search.py` script. This file is generated when the `twtter_search.py` is run.
- *example.env*: Holds variables for program (this is an example, so fields need to be populated)
- *twitter_search.py*: Uses the `/search` endpoint to retrieve tweets
- *twitter_stream.py*: Uses the `/stream` endpoint to retrieve tweets
- *utils/couchdb_driver.py*: Handles communication with couchdb
- *utils/file_driver.py*: Handles file_io
- *utils/process_tweets.py*: Handles processing of tweets (sentiment analysis)
- *utils/slack_integration.py*: Handles logic for sending messages to slack
- *utils/twitter_filters.py*: Stores filters used calling twitter api (tags or location filters)

## Running the twitter harvester script

1. Install requirements
   ``` shell
   pip3 install -r requirements.txt 
   ```
2. **Set up the Environment variables**: Rename `example.env` to `.env` and add the Twitter and slack variables (Slack variable is optional)
   
3. Run
   ``` shell
   python3 twitter_search.py
   ```
   The script will append tweets to `debug.out` and generate a `checkpoint.pickle` file

Note: Please don't push the twitter API keys to the repo (its considered bad practice) 