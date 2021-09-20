'''
@author: Souvik Das
Institute: University at Buffalo
'''

import demoji, re, datetime
import preprocessor


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet, poi):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        raw = tweet._json;
        country = {"en":"USA", "es": "Mexico", "hi": "India"}
        valid_languages = ["en", "es", "hi"]
        if raw['lang'] not in valid_languages:
            return {};
        dict = {}
        dict['poi_name'] = raw['user']['screen_name']
        dict['poi_id'] = raw['user']['id']
        dict['verified'] = raw['user']['verified']
        if(len(poi)):
            dict['country'] = poi['country']
        else:
            dict['country'] =   country[raw['lang']]  
        dict['id'] = raw['id_str']
        if len(poi):
            cleansedText = _text_cleaner(raw['full_text']);
            dict['tweet_text'] = raw['full_text']
        else:
            cleansedText = _text_cleaner(raw['text']);
            dict['tweet_text'] = raw['text']
        dict['tweet_lang'] = raw['lang']
        dict['text_'+raw['lang']] = cleansedText[0]
        if len(_get_entities(raw,'hashtags')):
            dict['hashtags'] = _get_entities(raw,'hashtags')
        if len(_get_entities(raw,'mentions')):    
            dict['mentions'] = _get_entities(raw,'mentions')
        if len(_get_entities(raw,'urls')):    
            dict['tweet_urls'] = _get_entities(raw,'urls')
        if len(cleansedText[1]):    
            dict['tweet_emoticons'] = cleansedText[1]
        dict['tweet_date'] = str(_get_tweet_date(raw['created_at']))
        if raw['geo'] != None:
            dict['geolocation'] = raw['geo']

        ### For Replies
        # dict['replied_to_tweet_id'] = raw['']           # pending
        # dict['replied_to_user_id'] = raw['']            # pending
        # dict['reply_text'] = raw['']                    # pending
        
        return dict;


def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet['entities']['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet['entities']['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet['entities']['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))
