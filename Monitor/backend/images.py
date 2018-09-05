"""
Monitor backend
File: images.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Loading image names and sending images to frontend.
"""
from .patterns import *
from liberouterapi import auth

import os
import json
import fnmatch
import re

from flask import send_from_directory

# TODO: Call load_image multiple times based on file names (Send names to frontend? => Frontend will call image loading)

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
    # We are loading dashboard images, no need to load patterns.
    if pattern_title == 'default':
        return get_user_images()

    patterns = json.loads(get_patterns())
    selected_pattern = None
    munin_folder = get_munin_folder()
    for pattern in patterns:
        if pattern['title'] == pattern_title:
            selected_pattern = pattern['pattern']
            break
    if selected_pattern is not None:
        filenames = []
        if '/' in selected_pattern:
            # pattern contains subdirectory, we need to use os.walk
            pathpattern, filepattern = os.path.split(selected_pattern)

            for path, subdirs, files in os.walk(munin_folder):
                # Path could be regex, multiple directories might match
                if re.match('.*[/]?' + pathpattern, path) is not None:
                    regex = re.compile(filepattern)
                    localpath = path.replace(munin_folder, "")
                    filenames = filenames + [localpath + '/' + f for f in filter(regex.search, files) if fnmatch.fnmatch(f, '*.png')]
        else:
            # pattern is not for subdirectory, listdir is enough
            regex = re.compile(selected_pattern)
            filenames = [f for f in filter(regex.search, os.listdir(munin_folder)) if fnmatch.fnmatch(f, '*.png')]
        return json.dumps(filenames)

    else:
        # fallback option for invalid patterns
        return get_user_images()

# Returns user-selected graph names from database.
@auth.required()
def get_user_images():
    # TODO: Implement this
    return [];


# Send image from disk to frontend.
@auth.required()
def load_image(filename):
    # TODO: Check if file is an image
    return send_from_directory(get_munin_folder(), filename)
