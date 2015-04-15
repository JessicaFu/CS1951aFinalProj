import oauth2 as oauth
import urllib2 as urllib
import json
import sys
import csv

_debug = 0

access_token_key = "3063624497-XzVwDr2bh8hCC56Advl8CVjIfH7dMhb82ZVRVUa"
access_token_secret = "P5msNxQA37fmIcougeC7IbCppYuqZZ4UUtLCWxcjZcjP4"

consumer_key = "U6r8fawMkwPfiUvLLyx3x08di"
consumer_secret = "rlZMpI7ZoDwtSbs3MT0Z8sJHSYaY15ybpw2GjAsUTCL19lPiqU"

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetch_by_user_name(userName):

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    parameters = [("screen_name", userName), ("count", 100)]
    response = twitterreq(url, "GET", parameters)
    for line in response:
        tweetList = json.loads(line)
        for tweet in tweetList:


        	tweet_author = userName
        	#I haven't done any tweet cleanup, like we do in the current classification assignment. I can if we wan't to, but i'm not sure what we're going for.
            tweet_text = tweet["text"].encode("utf-8").strip().replace("\n", " ")
            #I'm not sure if this is in the format we want to store dates in.
            tweet_created_at = tweet["created_at"]


fetch_by_user_name("CNN")
fetch_by_user_name("BBCWorld")
#Add any other twitter accounts here