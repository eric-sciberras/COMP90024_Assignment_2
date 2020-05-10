
def process_tweets(tweets,city):
    # do the sentiment analysis suttf here
    for tweet in tweets:
        tweet['city'] = city
        print(f'{tweet["id_str"]},{tweet["created_at"]}')
    return tweets