"""
Monitor backend
File: userfile.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Create, edit and read files containing user's graph configuration.
If storage method in config is set to "mongodb", this file is not used.
"""
from liberouterapi import auth
from .images import *

import json
import os

# Get path to server root
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

@auth.required()
def get_images_by_user(user):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    data = {"images": []}
    with open(user_file, 'a+') as f:
        try:
            f.seek(0)
            data = json.load(f)
        except Exception as e: # File did not exist or was empty.
            f.seek(0)
            json.dump({"images": []}, f)
            data = {"images": []}
            f.truncate()
    # If something happened, file will be closed and empty json will be returned.
    return json.dumps(data["images"])



@auth.required()
def add_image_to_db(user, filenames):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    with open(user_file, 'r+') as f:
        data = json.load(f)
        if data == None: # File did not exist or was empty.
            data = {"images": []}
        data["images"] = data["images"] + filenames
        f.seek(0)
        json.dump(data, f)
        f.truncate()

@auth.required()
def reorder_graphs(user, new_order):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    with open(user_file, 'w+') as f:
        json.dump({"images": new_order}, f) #TODO: Check data format

@auth.required()
def remove_graph(user, graph_name):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    with open(user_file, 'r+') as f:
        data = json.load(f)
        data["images"] = [d for d in data["images"] if d != graph_name]
        f.seek(0)
        json.dump(data, f)
        f.truncate()
