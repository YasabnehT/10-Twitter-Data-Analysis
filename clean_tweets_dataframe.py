import pandas as pd
import numpy as np
class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        # identify duplicates with id
        df.drop_duplicates(subset = 'id', keep=False,inplace=True)
        df = df[df['id'] != 'id']
        return df
    def convert_to_datetime(self, df:pd.DataFrame,tweets)->pd.DataFrame:
        """
        convert column to datetime
        """
        df = pd.DataFrame(data =[tweet.text for tweet in tweets], columns="tweets")
        df["id"] = np.array([tweet.id]for tweet in tweets)
        df['text'] = np.array([tweet.text for tweet in tweets])
        df['text_leng'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
        # df[df['created_at']] = pd.to_datetime(df[df['created_at']],format="%Y-%m-%d")
        # df = df[df['created_at'] >= '2022-07-31' ]
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.DataFrame('polarity')
               
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        # can be solved using the lang parameter from the live tweet
        # the json is filtered
        df = df[df['full_text']['lan' == 'en']]
        return df