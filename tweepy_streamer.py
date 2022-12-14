from tweepy.streaming import StreamListener
from tweepy import OAuthHanndler
from tweepy import Stream
from tweepy import API, Cursor # for data pagination
import pandas as pd
import numpy as np
from textblob import TextBlob # to clean the tweet and analyze sentiment
import re # regular expression
import twitter_credentials

### Use Cursor to extract timeline tweets from friends or yours ###
### Twitter Client Class ###
class TwitterClient():
    def __init__(self, twitter_user = None): # if no user, own timeline
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client
    def get_user_timeline_tweets(self, num_tweets):
        tweets = [] 
        for tweet in Cursor(self.twitter_client.user_timeline, id= self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    def get_friend_list(self, num_friends):
        friend_list = []
        # use id  = self.twitter_user for other users
        for friend in Cursor(self.twitter_client.friends).item(num_friends):
            friend_list.app(friend)
        return friend_list
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        # use id= self.twitter_user for other users
        for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

### Twitter Authenticator ###
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHanndler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        
 
### Twitter Streamer ###
class TwitterStreamer(): # streams twittes
    '''
    class for streaming and processing live tweets
    '''
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
  
    def stream_tweets(self,fetched_tweets_filename,has_tag_list):
        # handles twitter authentication and connection to Twitter streaming API
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        # stream.filter(track=['donald trumpm','hillary clinton', 'barack obama','bernie sanders'])
        stream.filter(track=has_tag_list)
		

class TwitterListener(StreamListener):
    '''
    basic listener class that prints recieved tweets to stdout
    '''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    def on_data(self, data):
       try:
           print(data)
           with open(self.fetched_tweets_filename, 'a') as tf:
               tf.write(data)
           return True
       except BaseException as e:
           print("print error on data:%s" %str(e))


    def on_error(self, status):
        # let the twitter API read limits the error message displayed
        # may take some time to re-visit the tweets
        if status ==420:
            # kill the proces if on-data method gets rate limit
            return False 
        print(status)


class TweetAnalyzer():
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:/\/\S+)"," ",tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet)
        
        if analysis.sentiment.polarity > 0:
            return 1 # positive sentiment
        elif analysis.sentiment.polarity == 0:
            return 0 # neutral sentiment
        else:
            return -1 #negative sentiment
            
    # analyze and categorize content from tweet
    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(data =[tweet.text for tweet in tweets], columns="tweets")
        df["id"] = np.array([tweet.id]for tweet in tweets)
        df['text'] = np.array([tweet.text for tweet in tweets])
        df['text leng'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
        return df
        
if __name__ == "__main__":
    # prints screened tweets from a user
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=20)
    df= tweet_analyzer.tweets_to_dataframe(tweets)
    # print(df.head) # print the first tweet texts
        
    """
    dataframe generation and ploting section        
    """
    
    # print(dir(tweets[0])) # possible field from the first tweet
    # print(tweets[0].id) # id of the first tweet
    # print(tweets[0].retweet_count) # number of retweets for the first tweet
    # print(tweets[0].favorite_count) # num positive sentiments
    # # print(tweets)
    
    
    # hash_tag_list =  ['donald trumpm','hillary clinton', 'barack obama','bernie sanders']
    # fetched_tweets_filename = "tweets.json"
    # #twitter_streamer = TwitterStreamer()
    # #twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
    # # for twitter_client
    # #twitter_client = TwitterClient()
    # twitter_client  = TwitterClient('Pycon') # username = pycon
    # # gets 5 user timeline tweets
    # print(twitter_client.get_user_timeline_tweets(5))
    
    """
    Sentiment analysis section
    """
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    print(df.head())

