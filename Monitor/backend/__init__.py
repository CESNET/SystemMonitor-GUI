"""
Monitor backend
File: __init__.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Backend initialization using liberouter GUI.
"""

from liberouterapi import config, modules
from liberouterapi.dbConnector import dbConnector

# Get Netopeer backend config
config.load(path = __path__[0] + '/config.ini')

db_conn = dbConnector("monitor",
        provider = "mongodb",
        config = {
            'database' : config['monitor']['database']
            })


# Register a blueprint
module_bp = modules.module.Module('monitor', __name__, url_prefix = '/monitor', no_version = True)


from .patterns import *
from .communications import *
from .db import *

# Returns patterns and their names from config
module_bp.add_url_rule('/patterns', view_func = get_patterns, methods = ['GET'])
# Sends image to frontend using send_from_directory()
module_bp.add_url_rule('/graph/<path:filename>', view_func = load_image, methods = ['GET'])
# Returns list of image paths based on pattern title
module_bp.add_url_rule('/filenames/<pattern_title>', view_func = load_filenames, methods = ['GET'])
# Returns list of image paths with interval filtering. Body of request should contain list of intervals in parameter intervals.
module_bp.add_url_rule('/filenames-filter/<pattern_title>', view_func = load_filenames_with_interval, methods = ['POST'])
# Returns list of image paths from DB by username. Can also be accessed by sending value 'default' to path /filenames/
module_bp.add_url_rule('/user', view_func = get_user_images, methods = ['GET'])
# Adds graph name to user's database entry. Graph is autmatically added to user sending this request.
# Graph list should be in request body.
module_bp.add_url_rule('/add-graph', view_func = add_user_images, methods = ['POST'])
