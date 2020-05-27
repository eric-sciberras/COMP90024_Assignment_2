from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
# Process tweet takes a python dictionary (the raw twitter json) and adds
# sentiment analysis and the city field
def process_tweet(tweet,city):
    # do the sentiment analysis stuff here
    try:
        sentiment = analyser.polarity_scores(tweet['full_text'])
    except:
        sentiment = analyser.polarity_scores(tweet['text'])
    
    tweet['sentiment'] = sentiment['compound']
    tweet['location'] = city
    return tweet


# For testing locally
# import json
# with open('processed_tweets.json','w') as out:
#     with open('debug_stream.json.bak','r') as f:
#         for (i,tweet) in enumerate(f.readlines()):
#             print(i)
#             # I just put a placeholder for city
#                 # json loads to convert string to dictionary
#                 # json dumps to convert dictionary to string
#             out.write(json.dumps(process_tweet(json.loads(tweet),"city")) + '\n' )

