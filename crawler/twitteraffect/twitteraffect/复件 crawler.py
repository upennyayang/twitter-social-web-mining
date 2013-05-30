#!/usr/bin/python

import time
import pycurl
import urllib
import json
import oauth2 as oauth

import os,sys
from datetime import datetime
from threading import Thread


API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
USER_AGENT = 'TwitterStream 1.0'  # This can be anything really

# You need to replace these with your own values
OAUTH_KEYS = {'consumer_key': "XaQd6sBZSu5BuZ8Brzjg9g",
              'consumer_secret': "pFqqMc98dhJeusBCH62UaaTQnI3dWLSKfnZOVquTRU",
              'access_token_key': "1284383658-Yi4ANrKhzfGJGX4RK9aI7DJNt96QhkWAzDd5lkX",
              'access_token_secret': "54pHBMahwik6a9IEME7pEKdgOMlRZNLDzfIA3nnDYyc"}

# These values are posted when setting up the connection
POST_PARAMS = {'include_entities': 0,
               'stall_warning': 'true',
               'track': ':),:-),:D,:-D'}
               #'track': ':)'}


TWEETS_PER_FILE=1000


class TwitterStream:
    def __init__(self, timeout=False):
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.buffer = ''
        self.timeout = timeout
        self.setup_connection()
        self.results = []  # Crawling results of tweets

        self.tweetsCount=0


    def setup_connection(self):
        """ Create persistant HTTP connection to Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.conn = pycurl.Curl()
        #self.conn.setopt(pycurl.CONNECTTIMEOUT, 3)    ### delete this if continuing crawing
        #self.conn.setopt(pycurl.TIMEOUT, 3)           ### delete this if continuting crawing
        # Restart connection if less than 1 byte/s is received during "timeout" seconds
        if isinstance(self.timeout, int):
            self.conn.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            self.conn.setopt(pycurl.LOW_SPEED_TIME, self.timeout)
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        # Using gzip is optional but saves us bandwidth.
        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
        self.conn.setopt(pycurl.HTTPHEADER, ['Host: stream.twitter.com',
                                             'Authorization: %s' % self.get_oauth_header()])
        # self.handle_tweet is the method that are called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)

        self.conn.setopt(pycurl.SSL_VERIFYPEER, 0)   
        self.conn.setopt(pycurl.SSL_VERIFYHOST, 0)

    def get_oauth_header(self):
        """ Create and return OAuth header.
        """
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': int(time.time())}
        req = oauth.Request(method='POST', parameters=params, url='%s?%s' % (API_ENDPOINT_URL,
                                                                             urllib.urlencode(POST_PARAMS)))
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def start(self):
        """ Start listening to Streaming endpoint.
        Handle exceptions according to Twitter's recommendations.
        """
        backoff_network_error = 0.25
        backoff_http_error = 5
        backoff_rate_limit = 60
        while True:
            self.setup_connection()
            try:
                self.conn.perform()
            except:
                # Network error, use linear back off up to 16 seconds
                print 'Network error: %s' % self.conn.errstr()
                print 'Waiting %s seconds before trying again' % backoff_network_error
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                # continue
                break    ### change to continue to continuing crawling
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                print 'Rate limit, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                print 'HTTP error %s, %s' % (sc, self.conn.errstr())
                print 'Waiting %s seconds' % backoff_http_error
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)

    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint.
        """
        self.buffer += data
        if data.endswith('\r\n') and self.buffer.strip():
            # complete message received
            message = json.loads(self.buffer)
            self.buffer = ''
            if message.get('limit'):
                print 'Rate limiting caused us to miss %s tweets' % (message['limit'].get('track'))
            elif message.get('disconnect'):
                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
            elif message.get('warning'):
                print 'Got warning: %s' % message['warning'].get('message')
            else:
                #print 'Got tweet with text: %s' % message.get('text').encode('gbk','ignore')
                self.results.append(message.get('text').encode('gbk','ignore'))    ### append tweets within some timeout
                self.tweetsCount+=1
                if self.tweetsCount == TWEETS_PER_FILE:
                    #self.result_to_file()
                    t=Thread(target=result_to_file,args=(list(self.results),))
                    t.start()
                    self.results=[]
                    self.tweetsCount=0
                    

    def get_result(self):
        return self.results

def result_to_file(copy_results):
    #copy_result
    tsp=datetime.now()
    fn=os.sep.join(['..','raw_data',POST_PARAMS['track'].replace(':',''),'result_'+ datetime.now().__str__().replace(' ','_').replace(':','-')])
    f=open(fn,'w')
    for item in copy_results:
        f.write('%s\n'%item)
    f.close()
    print fn
    copy_results=[]


if __name__ == '__main__':
    if len(sys.argv)==2:
        POST_PARAMS['track']=sys.argv[1]
    ts = TwitterStream()
    ts.setup_connection()
    ts.start()