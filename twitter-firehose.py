import boto3
import json
from datetime import datetime
import calendar
import random
import time
import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
consumer_key = ''
consumer_secret =''
access_token = ''
access_token_secret = ''


class TweetStreamListener(StreamListener):        
    # on success
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            if 'text' in tweet.keys():
                #print (tweet['text'])
                # message = str(tweet)+',\n'
                message = json.dumps(tweet)
                message = message + ",\n"
                print(message)
                kinesis_client.put_record(
                    DeliveryStreamName=stream_name,
                    Record={
                    'Data': message
                    }
                )
        except (AttributeError, Exception) as e:
                print (e)
        return True
        
    # on failure
    def on_error(self, status):
        print(status)


stream_name = ''  # fill the name of Kinesis data stream you created

if __name__ == '__main__':
    # create kinesis client connection
    kinesis_client = boto3.client('firehose',
                                  region_name='',  # enter the region
                                  aws_access_key_id='',  # fill your AWS access key id
                                  aws_secret_access_key='')  # fill you aws secret access key
    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()
    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # create instance of the tweepy stream
    stream = Stream(auth, listener)
    # search twitter for tags or keywords from cli parameters
    query = sys.argv[1:] # list of CLI arguments 
    query_fname = ' '.join(query) # string
    stream.filter(track=query)


