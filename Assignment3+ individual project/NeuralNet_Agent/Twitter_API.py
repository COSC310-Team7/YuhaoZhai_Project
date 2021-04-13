# # Twitter API

# pip install tweepy

import tweepy
import pandas as pd
import time

#use own credentials from twitter developer account
consumer_key = "cyURof8onxNo63Tdbc8d3mB4T"
consumer_secret = "JnKzJsPuLxi0Fa7BB26l7XTpwOYnoXD37Rqio0SpWsLi7QPN1n"
access_token = "1220785803078643713-9tG4OWTEa3ykTPm26l59uUd2nsYXfB"
access_token_secret = "TXpiUcgHfcBcvBpp2m9Zib0FDdZfw0ziPOyCeY27IGFJ5"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

username = 'JustinTrudeau'
count = 10

tweets = []
  
tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)

tweets_list = [[tweet.created_at, tweet.id,tweet.user.name,tweet.user.description, tweet.text,tweet.retweet_count] for tweet in tweets]
tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id','Username','Description' ,'Text','Retweets'])
tweets_df.to_csv('{}.csv'.format(username), sep=',', index = False)

