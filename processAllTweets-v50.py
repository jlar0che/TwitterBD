# Version .5
# Last Updated 10/31/2016

import json # For displaying API responses as pretty-printed JSON
import tweepy # Python library for accessing the Twitter API (Documentation here --> http://tweepy.readthedocs.io/en/v3.5.0/ )
import time # Allows us to slow down the queries to the API
from geopy.geocoders import GoogleV3 # Allows us to work with Logitude and Latitude data (More Info Here --> https://pypi.python.org/pypi/geopy/1.11.0 and Documentation here --> http://geopy.readthedocs.io/en/latest/)
import unicodedata # Work with Unicode data
import re

# Fix for printing to console errors
import sys
import codecs

import pprint # Gives us the ability to "Pretty Print" (Documentation here --> https://docs.python.org/2/library/pprint.html) NOTE: This is part of the standard library

# Add blank space for easier reading of output
print ""


# Fix for printing to console errors
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# Assign all pertinent API info to connect to a Twitter account
consumer_key = 'ENTER CONSUMER KEY HERE'
consumer_secret = 'ENTER CONSUMER SECRET HERE'
access_token = 'ENTER ACCESS TOKEN HERE'
access_token_secret = 'ENTER ACCESS TOKEN SECRET HERE'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# For error handling
TweepError = tweepy.TweepError
RateLimitError = tweepy.error.RateLimitError

# Instatntiate Pretty Print
pretty = pprint.PrettyPrinter()

# Instantiate Dictionaries that will hold retrieved data
outputdict = {}
finaloutputdict = {}

# Instantiate the GeoPy Geolocator
geolocator = GoogleV3()

# Initialize counter that will show where we are in the loop
counter = 0

# Loop to get Twitter data
# DOCS INFO:
# ----------
# API.followers([id/screen_name/user_id][, cursor])
# Returns an user's followers ordered in which they were added 100 at a time.
# If no user is specified by id/screen name, it defaults to the authenticated user.
for follower in tweepy.Cursor(api.followers, screen_name="ENTER TWITTER NAME HERE").items():

	# To go through more statuses per follower simply increase the count variable below
	# DOCS INFO:
	# ----------
	# API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
	# Returns the 20 most recent statuses posted from the authenticating user or the user specified.
	# It's also possible to request another user's timeline via the id parameter.
	print follower.screen_name

	try:
		retrievedStatuses = api.user_timeline(id = follower.id, count = 100)
		counter += 1
		print counter
		if counter >= 100:
			break
		# Save the first coordinates associated with follower into the 'outputdict' dictionary.
		# If coordinates are already in the dictionary then break the loop and move on.
		for tweet in retrievedStatuses:
			if follower.id in outputdict:
				if outputdict[follower.id] != None:
					break
				elif tweet.coordinates != None:
					print "Overriting 'None' entry in outputdict with: " + str(tweet.coordinates)
					outputdict[follower.id] = tweet.coordinates
					print "Entry made: " + str(outputdict)
					#print "The type for this entry is: "
					#print type(outputdict)
					print ""
			else:
				if tweet.coordinates != None:
					print "Putting " + str(tweet.coordinates) + " into outputdict"
					outputdict[follower.id] = tweet.coordinates
					print "Entry made: " + str(outputdict)
					#print "The type for this entry is: "
					#print type(outputdict)
					print ""
			# Wait a few seconds between requests in order to avoid Rate Limiting
			#time.sleep(2)
	except TweepError:
		print "TweepError... search me."
	except RateLimitError:
		time.sleep(60 * 15)
        continue

# Pretty Print the outputdict
print "Printing dictionary 'outputdict':"
pretty.pprint(outputdict)
print ""

# Pull out Zip codes from the retrieved coordinates and save that in a dictionary called 'finaloutputdict'
for k in outputdict:
	if outputdict[k] == None:
		pass
	else:

		try:
			print "outputdict [u'coordinates'] is:"
			print outputdict[k][u'coordinates']
			coordinate = outputdict[k][u'coordinates'] # Save coordinates from dictionary to variable called 'coordinate'
			print "Reversing coordinates (for correct input in GeoPy)"
			coordinate.reverse()
			print ""
			print "Saved reversed coordinates to variable 'coordinate':"
			print coordinate
			print ""

			location = geolocator.reverse(coordinate, exactly_one = True) # Use GeoPy to turn the coordinates into an Address. Save as variable 'location'
			print "Location pulled from GeoPy via geolocator.reverse(coordinate, exactly_one = True):"
			print location
			print ""

			address = unicodedata.normalize('NFKD', location[0]).encode('ascii','ignore') # Clean up the address and save al 'address'
			print "Cleaned Up Address via unicode.normalize"
			print address
			print ""

			re.search(\d)
			addressList = address.split(',') # More cleanup of 'address', saving that result as 'addressList'
			print "Split Address"
			print addressList
			print ""

			if " USA" in addressList:
				stateAndZip = addressList[2] # Pull the Sate and Zip out of the Geolocated address
				print "State and Zip pulled from 'addressList'"
				print stateAndZip
				print ""
				print "'USA' found"
				print ""

				zipCode = int(filter(str.isdigit, stateAndZip)) # Pull out the Zip Code from the State and Zip
				print "Zipcode pulled from that... "
				print zipCode
				print ""

				finaloutputdict[k] = zipCode # Put the Zip code in the dictionary 'finaloutputdict'
				print "ZipCode put into final dictionary"
				print finaloutputdict[k]
				print ""
				print "<--- End Loop --->"
				print ""
			else:
				stateAndZip = addressList[2] # Pull the Sate and Zip out of the Geolocated address
				print "State and Zip pulled from 'addressList'"
				print stateAndZip
				print ""
				print "'USA' not found"
				print ""

				pass
		except(TypeError, IndexError):
			pass #pass if there are any errors


# Pretty Print the finaloutputdict
print "Printing dictionary 'finaloutputdict':"
pretty.pprint(finaloutputdict)
print ""
