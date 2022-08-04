import os 
import logging
from pathlib import Path
from distutils.dir_util import copy_tree
from gvars import *


def init_ui():
    """ Create workspace UI if it does not exist yet
    """
    if not Path(WORKSPACE_UI_DIR).is_dir():
        logging.info('This workspace has no UI folder, initiating...')
        this_path = os.path.dirname(os.path.realpath(__file__))
        copy_tree(f"{this_path}/ui", WORKSPACE_UI_DIR)
        logging.info('UI initiated')
    else:
        logging.info('This workspace already has UI initiated')