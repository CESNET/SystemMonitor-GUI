"""
Monitor backend
File: images.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Generation of image names from patterns and filtering them.
"""
from .patterns import *
from .db import *
from liberouterapi import auth

import os
import json
import fnmatch
import re


def get_munin_folder():
    """ Load munin installation location from config """
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'patterns.json')
    data = json.load(open(json_url))
    # TODO: Check if directory exists to prevent crashes, notify user
    return data['munin-path']

def add_interval_filter(intervals, pattern):
    """
        Add intervals to pattern to load only graphs in given interval.

        Arguments:
         intervals -- array of interval names. Valid names are day, week, month, year
         pattern -- pattern to add interval pattern to.

        Returns:
         New pattern that includes interval filtering
    """
    if interval != []:
        pattern = pattern + "-(" + intervals[0]
        for i in range(1, len(intervals)):
            pattern = pattern + '|' + intervals[i]
        pattern = pattern + ')'
    return pattern


@auth.required()
def names_from_patterns(pattern):
    """ Returns array of file names based on pattern. """
    # We are loading dashboard images, skip rest of this function
    if pattern == None:
        return get_user_images()
    else:
        munin_folder = get_munin_folder()
        filenames = []
        if '/' in pattern:
            # pattern contains subdirectory, we need to use os.walk
            pathpattern, filepattern = os.path.split(pattern)

            for path, subdirs, files in os.walk(munin_folder):
                # Path could be regex, multiple directories might match
                if re.match('.*[/]?' + pathpattern, path) is not None:
                    regex = re.compile(filepattern)
                    localpath = path.replace(munin_folder, "")
                    filenames = filenames + [localpath + '/' + f for f in filter(regex.search, files) if fnmatch.fnmatch(f, '*.png')]
        else:
            # pattern is not for subdirectory, listdir is enough
            regex = re.compile(pattern)
            filenames = [f for f in filter(regex.search, os.listdir(munin_folder)) if fnmatch.fnmatch(f, '*.png')]
        return json.dumps(filenames)


@auth.required()
def get_user_images():
    """ Returns user-selected graph names from database. """
    session = auth.lookup(request.headers.get('lgui-Authorization', None))
    user = session['user']
    return json.dumps(get_images_by_user(user))
