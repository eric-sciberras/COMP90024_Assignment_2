from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Process tweet takes a python dictionary (the raw twitter json) and adds
# sentiment analysis and the city field
def process_tweet(tweet,city):
    # do the sentiment analysis stuff here
    analyser = SentimentIntensityAnalyzer()
    sentiment = analyser.polarity_scores(tweet)
    
    tweet['sentiment'] = sentiment
    tweet['city'] = city
    return tweet


# For testing locally
import json
with open('../test_data/tweets.json','r') as f:
 for tweet in f.readlines():
    print(tweet)
    # I just put a placeholder for city
    with open('processed_tweets.json','w') as out:
        # json loads to convert string to dictionary
        # json dumps to convert dictionary to string
        out.write(json.dumps(process_tweet(json.loads(tweet),"city")))

