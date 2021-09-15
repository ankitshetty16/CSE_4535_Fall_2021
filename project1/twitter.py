'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("q5pqB8ajkb618RWBlte6AbckO", "m6pHFxNoX41tr8VXhcodSYwgO2xIWQCvU6Zuof0JoShsG8RFqa")
        self.auth.set_access_token("1432461231680598022-k4xCu47h0qJu8klui9t5gLpZ1XCBFT", "5EYJmAwzNThDMejPCQso7iF1vTBWYmB4103zUeW3E2yJ4")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        raise NotImplementedError

    def get_tweets_by_poi_screen_name(self):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        raise NotImplementedError

    def get_tweets_by_lang_and_keyword(self):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        raise NotImplementedError

    def get_replies(self):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        raise NotImplementedError
