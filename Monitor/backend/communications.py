"""
Monitor backend
File: communications.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Handling communications between frontend and backend
"""

from liberouterapi import auth

from .patterns import *
from .images import *
import json

from flask import send_from_directory

@auth.required()
def load_image(filename):
    """ Send image from disk to frontend. """
    return send_from_directory(get_munin_folder(), filename)

@auth.required()
def load_filenames(pattern_title):
    """ Load image names based on pattern title """
    return names_from_patterns(pattern_from_name(pattern_title))

@auth.required()
def load_filenames_with_interval(pattern_title, intervals):
    """ Load image names with interval filtering """
    return names_from_patterns(add_interval_filter(intervals, pattern_from_name(pattern_title)))
