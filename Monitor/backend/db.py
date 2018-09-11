"""
Monitor backend
File: db.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Database connections
"""

from liberouterapi import db, auth, config
from liberouterapi.dbConnector import dbConnector

from .images import *

import json
from flask import jsonify

monitor = dbConnector('monitor')
db = monitor.db[config['monitor']['collection']]
user_graphs = db.user_graphs

@auth.required()
def get_images_by_user(user):
    """ Returns list of graph file names of given user """
    res = user_graphs.find_one({'user': user})
    if res == None:
        return json.dumps([])
    images = res['images']
    # result = decompile_db_strng(images)
    return images

@auth.required()
def add_image_to_db(user, filenames):
    """ Adds an image to user's list of graphs

        Arguments:
         user -- username of logged-in user
         filenames -- list of names to add. If you want to add one image, use list with one item.
    """
    # Add semicolon and filename to db string by user.
    # If user was not in DB, create row for him and add filename without semicolon
    # filenames is an array, to add one graph input array with one item
    # this simplifies adding multiple graphs (multiple intervals at once)
    # IDEA: If this is too slow, frontend could add new graphs to some buffer and send them to db when page is unloading.
    # IDEA: If that is the case, some flag should indicate, that graphs changed.

    res = user_graphs.find_one({'user': user})
    if res == None:
        images = []
    else:
        images = res['images']
    #result = create_db_string(images, filenames)
    images = images + filenames
    user_graphs.update_one({"user": user }, {'$set': {"images": images}}, True)



@auth.required()
def reorder_graphs(user, new_order):
    user_graphs.update_one({"user": user }, {'$set': {"images": new_order}}, True)

@auth.required()
def remove_graph(user, graph_name):
    old_graphs = get_images_by_user(user)
    graphs = [x for x in old_graphs if x != graph_name]
    reorder_graphs(user, graphs)
