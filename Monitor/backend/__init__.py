"""
Monitor backend
File: __init__.py
Author: Jakub Man <xmanja00@stud.fit.vutbr.cz>

Backend initialization using liberouter GUI.
"""

from liberouterapi import config, modules


# Register a blueprint
module_bp = modules.module.Module('monitor', __name__, url_prefix = '/monitor', no_version = True)


from .patterns import *
from .images import *

module_bp.add_url_rule('/patterns', view_func = get_patterns, methods = ['GET'])
module_bp.add_url_rule('/graph/<image_name>', view_func = load_image, methods = ['GET'])
module_bp.add_url_rule('/filenames/<pattern_title>', view_func = names_from_patterns, methods = ['GET'])
