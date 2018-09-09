"""
Monitor backend
File: db.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Database connections
"""

from liberouterapi import db, auth, config
from liberouterapi.dbConnector import dbConnector

from .images import *

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
    return json.dumps(images.split(';'))

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
    res = db.find_one({'user': user})
    if res == None:
        # User was not found, add him
        result = create_db_string('', filenames)
        user_graphs.insert_one({"user": user, "images": result})
    else:
        images = res['images']
        result = create_db_string(images, filenames)
        user_graphs.update_one({"user": user }, {"images": result})


@auth.required()
def reorder_graphs(user, new_order):
    # This function will simply replace old string with new string.
    # This can be useful in GUI, where user should be able to reorder his graphs
    # IDEA: Frontend would change array imagesToShow[] and send it to backend.
    # IDEA: There should be a boolean indicating change, changes should be sent when unloading page.
    pass
