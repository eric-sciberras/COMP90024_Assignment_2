# COMP90024_Assignment_2

## Running the twitter harvester script

1. **Set up the Environment variables**: Rename `example.env` to `.env` and add the Twitter and slack variables (Slack variable is optional)
   
2. Run
   ``` shell
   python3 twitter_streamer.py
   ```
   The script will append the whole tweet object to a file `stream_output_au.txt` and also print out incoming tweet text.

Note: Please don't push the twitter API keys to the repo (its considered bad practice) 