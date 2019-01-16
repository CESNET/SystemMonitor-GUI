"""
Monitor backend
File: patterns.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Loading patterns for getting graphs from Munin.
"""
from liberouterapi import auth

import os
import json

@auth.required()
def get_patterns():
    """ Load patterns from config file and return them as stringified JSON. """
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'patterns.json')
    data = json.load(open(json_url))
    output_dict = [x for x in data['patterns'] if x['enabled'] == 'true']
    return json.dumps(output_dict)


def pattern_from_name(pattern_title):
    """ Load pattern from pattern title """
    selected_pattern = None
    for pattern in json.loads(get_patterns()):
        if pattern['title'] == pattern_title:
            selected_pattern = pattern['pattern']
            break
    return selected_pattern
