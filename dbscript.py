from pymongo import MongoClient

# Connect and find/create database
client = MongoClient('localhost', 27017)
db = client['IxP']

# Init collection
user_collection = db['user']
route_collection = db['route']
location_collection = db['location']


"""
User Collection:

{
	username: String,
	profilePicture: BLOB,
	password: Hashed password,
	firstName: String,
	lastName: String,
	routes: [route-id]
}

Route Collection:

{
	route-id: (generated by mongodb),
	locations: [{location-id: Number,  dayOfTravel: String}]
}

Location Collection:

{
	location-id: (generated by mongodb),
	name: String,
	city: String,
	address: String,
	latitude: Number,
	longitude: Number,
	rating: Number,
	comments: [{user: String, comment: String}]
}



"""