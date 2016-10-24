# Version .4
# Last Updated 10/24/2016

import json # For displaying API responses as pretty-printed JSON
import tweepy # Python library for accessing the Twitter API (Documentation here --> http://tweepy.readthedocs.io/en/v3.5.0/ )
import time # Allows us to slow down the queries to the API
from geopy.geocoders import GoogleV3 # Allows us to work with Logitude and Latitude data
import unicodedata # Work with Unicode data

# Fix for printing to console errors
import sys
import codecs
import pprint

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# Assign all pertinent API info to connect to a Twitter account
consumer_key = 'ENTER YOUR CONSUMER KEY HERE'
consumer_secret = 'ENTER YOUR CONSUMER SECRET KEY HERE'
access_token = 'ENTER YOUR ACCESS TOKEN HERE'
access_token_secret = 'ENTER YOUR ACCESS TOKEN SECRET HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


pretty = pprint.PrettyPrinter()
outputdict = {}
finaloutputdict = {}

# Instantiate the Geolocator
geolocator = GoogleV3()

for follower in tweepy.Cursor(api.followers, screen_name="YOUR-TWITTER-NAME-HERE").items():
	last100 = api.user_timeline(id = follower.id, count = 100)

	for tweet in last100:
		if follower.id in outputdict:
			if outputdict[follower.id] != None:
				break
			else:
				outputdict[follower.id] =  tweet.coordinates
		else:
			outputdict[follower.id] = tweet.coordinates

pretty.pprint(outputdict)

for k in outputdict:
	if outputdict[k] == None:
		pass
	else:
		try:
			coordinate = outputdict[k][u'coordinates']
			location = geolocator.reverse(coordinate, exactly_one = True)
			address = unicodedata.normalize('NFKD', location[0]).encode('ascii','ignore')
			addressList = address.split(',')
			stateAndZip = addressList[2]
			zipCode = int(filter(str.isdigit, stateAndZip))
			finaloutputdict[k] = zipCode
		except(TypeError, IndexError):
			pass

pretty.pprint(finaloutputdict)
