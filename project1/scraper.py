'''
@author: Souvik Das
Institute: University at Buffalo
'''

import json
import datetime
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer

reply_collection_knob = False

def read_records():
    with open("records.json") as json_file:
        data = json.load(json_file)

    return data

def write_records(data):
    with open("records.json", 'w') as json_file:
        json.dump(data, json_file)    

def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")

def _update_records(records, lang, country):
    records['counter'][lang] = records['counter'][lang] + 1
    records['counter'][country] = records['counter'][country] + 1
    records['counter']['total'] = records['counter']['total'] +  1

    return records;

def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()

    records = read_records()
    pois = config["pois"]
    keywords = config["keywords"]

    for i in range(len(pois)):
        if pois[i]["finished"] == 0:
            print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")

            raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i])
            processed_tweets = []
            for tw in raw_tweets:
                processed = TWPreprocessor.preprocess(tw,pois[i])
                if processed != {}:
                    processed_tweets.append(processed)
                    records = _update_records(records, processed['tweet_lang'], processed['country'])
            indexer.create_documents(processed_tweets)

            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })
            write_records({
                "counter": records
            })

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")

    for i in range(len(keywords)):
        if keywords[i]["finished"] == 0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")

            raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i])

            processed_tweets = []
            for tw in raw_tweets:
                processed = TWPreprocessor.preprocess(tw,{})
                if processed != {}:
                    processed_tweets.append(processed)
                    records = _update_records(records, processed['tweet_lang'], processed['country'])

            indexer.create_documents(processed_tweets)

            keywords[i]["finished"] = 1
            keywords[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })
            write_records({
                "counter": records
            })            

            save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")

            print("------------ process complete -----------------------------------")

    if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.

        raise NotImplementedError


if __name__ == "__main__":
    main()
