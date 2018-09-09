"""
Monitor backend
File: db.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Database connections
"""

from liberouterapi import db, auth, config
from liberouterapi.dbConnector import dbConnector

monitor = dbConnector('monitor')
monitor = monitor.db[config['monitor']['collection']]

def images_from_db(user):
    """ Returns list of graph file names of given user in a list """
    pass
    # if entry in db doesnt exist, return empty array
    # return (explode string from db by ';')

def add_image_to_db(user, filenames):
    """ Adds an image to user's list of graphs """
    # Add semicolon and filename to db string by user.
    # If user was not in DB, create row for him and add filename without semicolon
    # filenames is an array, to add one graph input array with one item
    # this simplifies adding multiple graphs (multiple intervals at once)
    # IDEA: If this is too slow, frontend could add new graphs to some buffer and send them to db when page is unloading.
    # IDEA: If that is the case, some flag should indicate, that graphs changed.
    pass

def reorder_graphs(user, new_order):
    # This function will simply replace old string with new string.
    # This can be useful in GUI, where user should be able to reorder his graphs
    # IDEA: Frontend would change array imagesToShow[] and send it to backend.
    # IDEA: There should be a boolean indicating change, changes should be sent when unloading page.
    pass
