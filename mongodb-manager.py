import configparser
from pymongo import MongoClient
import csv
from datetime import datetime

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
all_recipes = list(recipes_collection.find({}))
#print(list(all_recipes))

all_fieldnames = set()

for recipe in all_recipes:
    all_fieldnames.update(recipe.keys())

all_fieldnames = list(all_fieldnames) 

print(all_recipes)

path = 'mongodb/'
now = datetime.today().strftime("%Y-%m-%d-%H%M%S")
filename = path + now + '_' +  'recipes' + '.csv'

with open(filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=all_fieldnames)
    writer.writeheader()

    for recipe in all_recipes:
        
        for field in all_fieldnames:
            recipe.setdefault(field, None)
            
        writer.writerow(recipe)


client.close()
