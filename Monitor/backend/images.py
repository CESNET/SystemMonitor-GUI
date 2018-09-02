"""
Monitor backend
File: images.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Sending images from server to frontend.
"""
from .patterns import *
from liberouterapi import auth

import os
import json
import fnmatch

# TODO: Call load_image multiple times based on file names (Send names to frontend?)

# Load munin installation location from config
def get_munin_folder():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'patterns.json')
    data = json.load(open(json_url))
    # TODO: Check if directory exists to prevent crashes
    return data['munin-path']

# Returns array of file names based on patterns from config.
@auth.required()
def names_from_patterns(pattern_title):
    patterns = json.loads(get_patterns())
    selected_pattern = None

    for pattern in patterns:
        if pattern['title'] == pattern_title:
            selected_pattern = pattern['pattern']
            break
    if selected_pattern is not None:
        filenames = []
        for file in os.listdir(get_munin_folder()):
            if fnmatch.fnmatch(file, selected_pattern)
                filenames.append(file)
        return filenames
    else:
        return get_user_images()

# Returns user-selected graph names from database.
@auth.required()
def get_user_images():
    # TODO: Implement this
    return [];


# Send image from disk to frontend.
@auth.required()
def load_image(filename):
    return send_from_directory(get_munin_folder(), filename)
