import configparser
from pymongo import MongoClient
import csv

# Initialize the configparser object and ead the configuration file
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

# Access the MongoDB URI and Connect to MongoDB Atlas using the URI
mongodb_uri = config['MONGODB']['URI'] 
client = MongoClient(mongodb_uri)

# Database operations
db = client.todayieat  
recipes_collection = db['recipes']

# Fetch all documents from the collection & print CSV
all_recipes = recipes_collection.find()


filtered_schema = set()
unique_schema = []
for recipe in all_recipes:
    schemas = recipe.keys()
    for schema in schemas:
        if schema not in filtered_schema:
            filtered_schema.add(schema)
            unique_schema.append(schema)
        
        
print(unique_schema)




#fieldnames = list(all_recipes[0].keys()) if all_recipes else []
#print(fieldnames[0])


client.close()
