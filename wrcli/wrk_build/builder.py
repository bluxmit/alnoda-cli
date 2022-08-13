import os 
# os.chdir('/home/project/workspace-cli/wrcli/wrk_build')
# this_path = '/home/project/workspace-cli/wrcli/wrk_build'
# conf_file = "/home/project/workspace-cli/tests/conf_parse/workspace-opt-field-miss-val.yaml"
# conf_dir_path = "/home/project/workspace-cli/tests/conf_parse/workspace-dirs/correct"
import logging
import json, yaml
from pathlib import Path
from distutils.dir_util import copy_tree
from .meta_about import update_meta_and_about
from .conf_parser import read_conf_dir
from ..globals import *

SUPERVISORD_FOLDER = "/etc/supervisord"

supervisord_template = """

"""


def init_wrk():
    """  ->> bool
    Check if this workspace has UI folder. If not copy the 
    boilerplate - the default starting UI
    """
    try:
        if not Path(WORKSPACE_DIR).is_dir():
            logging.info('Initiating workspace...')
            this_path = os.path.dirname(os.path.realpath(__file__))
            copy_tree(os.path.join(this_path, 'wrk'), WORKSPACE_DIR)
            # update meta 
            update_meta()   #<- only update created date
        else:
            logging.info('Workspace initialized')
    except:
        logging.critical("Something went wrong. Is workspace folder deleted?")
        return False
    return True


def add_startup_application():
    """
    Add command to start application
    """
    pass


def build_workspace(conf_dir_path):
    """ str ->>
    Builds/updates UI based on the cofigs folder provided by the user. 
    Config folder must have file ui_config.yaml, and all images that are used to the UI.

    :param conf_dir_path: path to the config directory
    :type conf_dir_path: str
    """
    initialized = init_wrk()  # <- First make sure UI is initiated
    if not initialized:
        raise Exception("There was a problem initializing workspace UI")
    # Read new user configs_dir
    wrk_params, files = read_conf_dir(conf_dir_path)
    # update meta.json and refresh About page 
    update_meta(
        name = wrk_params['name'],
        version = wrk_params['version'],
        author = wrk_params['author'],
        description = wrk_params['description']
    )
    refresh_about_from_meta()
    






