#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Based on: https://gist.github.com/yanofsky/5436496
# and https://www.twilio.com/blog/2016/09/fun-with-markov-chains-python-and-twilio-sms.html

import csv
import argparse
import os
import re
import tweepy


# Twitter API credentials
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_key = os.environ['TWITTER_ACCESS_KEY']
access_secret = os.environ['TWITTER_ACCESS_SECRET']


def clean_tweet(tweet):
    """
    Clean tweets from unnecessary characters and words
    """
    tweet = re.sub("https?\:\/\/", "", tweet)   # links
    tweet = re.sub("#\S+", "", tweet)           # hashtags
    tweet = re.sub("\.?@", "", tweet)           # at mentions
    tweet = re.sub("RT.+", "", tweet)           # Retweets
    tweet = re.sub("Video\:", "", tweet)        # Videos
    tweet = re.sub("\n", "", tweet)             # new lines
    tweet = re.sub("^\.\s.", "", tweet)         # leading whitespace
    tweet = re.sub("\s+", " ", tweet)           # extra whitespace
    tweet = re.sub("&amp;", "and", tweet)       # encoded ampersands
    return tweet


def write_tweets_to_csv(tweets, out_path='tweets.csv'):
    with open(out_path, 'wb') as f:
        writer = csv.writer(f)
        for tweet in tweets:
            tweet = clean_tweet(tweet)
            if tweet:
                writer.writerow([tweet])


def get_all_tweets(screen_name):
    all_tweets = []
    new_tweets = []
 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    client = tweepy.API(auth)
    new_tweets = client.user_timeline(screen_name=screen_name, count=200)
 
    while len(new_tweets) > 0:
        for tweet in new_tweets:
            if tweet.source == 'Twitter for Android':
                all_tweets.append(tweet.text.encode("utf-8"))
 
        print "%s tweets so far" % (len(all_tweets))
        max_id = new_tweets[-1].id - 1
        new_tweets = client.user_timeline(screen_name=screen_name,
                                          count=200, max_id=max_id)
 
    return all_tweets


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", required=True,
                        help="username of twitter account")
    parser.add_argument("-f", "--file", default='tweets.csv',
                        help="path to file where to store tweets")
    args = parser.parse_args()

    tweets = get_all_tweets(args.username)
    write_tweets_to_csv(tweets, args.file)
