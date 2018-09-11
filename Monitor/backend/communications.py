"""
Monitor backend
File: communications.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Handling communications between frontend and backend
"""

from liberouterapi import auth

from .patterns import *
from .images import *
from .db import *
import json

from flask import send_from_directory, request

@auth.required()
def load_image(filename):
    """ Send image from disk to frontend. """
    return send_from_directory(get_munin_folder(), filename)

@auth.required()
def load_filenames(pattern_title):
    """ Load image names based on pattern title """
    if pattern_title == 'default':
        return get_user_images()
    else:
        return names_from_patterns(pattern_from_name(pattern_title))

@auth.required()
def load_filenames_with_interval(pattern_title):
    """ Load image names with interval filtering """
    data = request.json
    intervals = data['intervals']
    return names_from_patterns(add_interval_filter(intervals, pattern_from_name(pattern_title)))

@auth.required()
def get_user_images():
    """ Returns user-selected graph names from database. """
    session = auth.lookup(request.headers.get('lgui-Authorization', None))
    user = session['user']
    return json.dumps(get_images_by_user(user.username))

@auth.required()
def add_user_images():
    session = auth.lookup(request.headers.get('lgui-Authorization', None))
    user = session['user']
    data = request.json
    images = data['images']
    add_image_to_db(user.username, images)
    return json.dumps([])

@auth.required()
def remove_user_image():
    session = auth.lookup(request.headers.get('lgui-Authorization', None))
    user = session['user']
    data = request.json
    graph = data['graph']
    remove_graph(user.username, graph)
    return json.dumps([])

@auth.required()
def reorder():
    session = auth.lookup(request.headers.get('lgui-Authorization', None))
    user = session['user']
    data = request.json
    graphs = data['graphs']
    reorder_graphs(user.username, graphs)
    return json.dumps([])
