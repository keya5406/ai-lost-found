import json
import os

# Set the path to your data folder
data_folder = 'data'
items_file = os.path.join(data_folder, 'items.json')

# Function to load the items from the file
def load_items():
    if not os.path.exists(items_file):
        return []
    with open(items_file, 'r') as f:
        return json.load(f)

# Function to save items to the file
def save_items(items):
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    with open(items_file, 'w') as f:
        json.dump(items, f, indent=4)
