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
def get_image_by_user(user):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    data = {}
    with open(user_file) as f:
        data = json.load(f)
    # If something happened, file will be closed and empty json will be returned.
    return json.dumps(data)



@auth.required()
def add_image_to_db(user, filenames):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    with open(user_file, 'r+') as f:
        data = json.load(f)
        data[0] = data[0] + filenames
        json.dump(data, f)

@auth.required()
def reorder_graphs(user, new_order):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    with open(user_file, 'w') as f:
        json.dump({new_order}, f) #TODO: Check data format

@auth.required()
def remove_graph(user, graph_name):
    user_file = os.path.join(SITE_ROOT, user + '.json')
    with open(user_file) as f:
        data = json.load(f)
        data = {[d for d in data[0] if d != graph_name]} #TODO: Check if this works
        json.dump(data, f)
    
