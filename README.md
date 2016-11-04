# TwitterBD
Using Python to work with Big Data sets from Twitter
====================================================

Version .50 <br />
 > Jacques Laroche <br />
 > Tim Ryan <br />
 > Steven Gilliam <br />

----------------------------------------------------
CONTENTS:
----------------------------------------------------

I. FEATURES
II. RELEASE NOTES
III. CONTACT INFORMATION


----------------------------------------------------
I. FEATURES
----------------------------------------------------

*	Retrieve the Followers of a Twitter account

*	Retrieve a specified number of tweets from each Follower

*	Perform Geolocation on these tweets
 

----------------------------------------------------
II. RELEASE NOTES
----------------------------------------------------
v.50:
-----
* Added Regex to parse address
* Added Loop Counter as visual aid when performing main loop

v.45:
-----
*  Added detailed comments throughout script.
*  Changed for loop to only process coordinate information if not null.
*  Added sleep timer to main loop in order to avoid Rate Limiting.
*  Fixed format of coordinates retrieved from Tweepy to work correctly with GeoPy.
*  Added numerous print statements to loops for debugging purposes.


<b>Technical Notes:</b>

Written in Python 2.7 
	The following packages are used:
	* geopy
	* oauthlib
	* requests
	* requests-oauthlib
	* six
	* tweepy
	
	Note: use 'pip install -r requirements.txt' to install all necessary packages at once 

----------------------------------------------------
III. CONTACT INFORMATION
----------------------------------------------------

Jacques Laroche <br />
https://currentperspectives.org/about
