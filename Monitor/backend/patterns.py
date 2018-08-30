"""
Monitor backend
File: patterns.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Loading patterns for getting graphs from Munin.
"""
from liberouterapi import auth

import os
import json

#Load patterns from config file and return them as JSON.
@auth.required()
def get_patterns():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'patterns.json')
    data = json.load(open(json_url))
    return json.dumps(data['patterns'])
