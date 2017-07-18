#GOOGLEPLACES API = AIzaSyCiT_v1UiAVzG3Shd4c5RxXxFncu5_d9YU

#YELP 
#Client ID: BaTsUsy-Le7IyQ5Yxd0kbw
#Client secret: 8wUuql7eDUpN8VSRlwmUMlpATTvBDgppDEmfOFynIA4NxitKIRrzrCHn1jovZUFY
"""
{
    "access_token": "mgE_trsR5CSJnSXU8bJXXI-wT4ks7KRY2bxOfgfsFOFvD__AwwSOpcuCRUVqskInyDaWoBBtMX3pQmfe7OinJHtc8jaMjFaIRkhih7jHDSESCOm2_NpYW_X-ZW5uWXYx",
    "expires_in": 15551999,
    "token_type": "Bearer"
}
"""

from flask import Flask, jsonify
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import requests
app = Flask(__name__)
geo_key = "AIzaSyBUwnh3e4nK8Emj02rYmAETs3SkSAsli2s"
places_key = "AIzaSyCiT_v1UiAVzG3Shd4c5RxXxFncu5_d9YU"
search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
access_token = "mgE_trsR5CSJnSXU8bJXXI-wT4ks7KRY2bxOfgfsFOFvD__AwwSOpcuCRUVqskInyDaWoBBtMX3pQmfe7OinJHtc8jaMjFaIRkhih7jHDSESCOm2_NpYW_X-ZW5uWXYx"
headers = {'Authorization': 'bearer %s' % access_token}
"""
auth = Oauth1Authenticator(
    consumer_key="BaTsUsy-Le7IyQ5Yxd0kbw",
    consumer_secret="8wUuql7eDUpN8VSRlwmUMlpATTvBDgppDEmfOFynIA4NxitKIRrzrCHn1jovZUFY",
    #token=YOUR_TOKEN,
    #token_secret=YOUR_TOKEN_SECRET
)
"""

#client = Client(auth)

@app.route("/geocoordinates")
def coordinates():
	search_url = ("https://maps.googleapis.com/maps/api/geocode/json?components=locality:san+francisco&key="+geo_key)
	search_result = requests.get(search_url)
	search_json_obj = search_result.json()
	return search_json_obj

@app.route("/fetchAreas")
def areas():
	gps_coordinates = coordinates()

	latitude = gps_coordinates['results'][0]['geometry']['location']['lat']
	longitude = gps_coordinates['results'][0]['geometry']['location']['lng']

	print('lat/long ' + str(latitude) + ' ' + str(longitude))
	places_url = ("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(latitude) + ", " + str(longitude) + "&radius=50&type=restaurant&key=" + places_key)
	places_result = requests.get(places_url)
	places_json = places_result.json()
	return jsonify(places_json)

@app.route("/autocomplete")
def autocomplete():
	input = "del"
	autocomplete_url = ("https://maps.googleapis.com/maps/api/place/autocomplete/json?input=" + input + "&key=" + places_key)
	autocomplete_result = requests.get(autocomplete_url)
	autocomplete_json = autocomplete_result.json()
	return jsonify(autocomplete_json)

@app.route("/yelp-auth")
def yelp_key():
	return

@app.route("/recommendations")
def fetchRecommendations():

	url = 'https://api.yelp.com/v3/businesses/search'
	headers = {'Authorization': 'bearer %s' % access_token}
	params = {'location': 'San Bruno',
          'term': 'Japanese Restaurant',
          'pricing_filter': '1, 2',
          'sort_by': 'rating'
         }

	resp = requests.get(url=url, params=params, headers=headers)
	search_json = resp.json()
	return jsonify(search_json)

if __name__ == "__main__":
    app.run()

