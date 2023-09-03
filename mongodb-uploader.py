import configparser
from pymongo import MongoClient
import csv
from datetime import datetime

# Initialize the configparser object and read the config file
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

# Connect to MongoDB Atlas
mongodb_uri = config['MONGODB']['URI']
client = MongoClient(mongodb_uri)

# Database operations
db = client.todayieat
recipes_collection = db['recipes']

# Counters for new and updated collections
new_collections = 0
updated_collections = 0

# Function to handle the CSV row based on 'recipeUrl'
def check_and_update_or_insert(recipe_row):
    global new_collections
    global updated_collections
    
    recipe_row["hidePicture"] = True if recipe_row["hidePicture"].lower() == "true" else False
    recipe_row["activate"] = True if recipe_row["activate"].lower() == "true" else False
    recipe_url = recipe_row.get('recipeUrl')
    existing_recipe = recipes_collection.find_one({"recipeUrl": recipe_url})

    if existing_recipe is None:
        recipes_collection.insert_one(recipe_row)
        new_collections += 1
    else:
        recipes_collection.update_one({"recipeUrl": recipe_url}, {"$set": recipe_row})
        updated_collections += 1

# Read the CSV file
with open('extracts/2023-09-01-104639_elavegan.com.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        check_and_update_or_insert(row)

client.close()

# Output the success message
print(f"Successfully added {new_collections} new collections and updated {updated_collections} existing collections.")
