import os 
# os.chdir('/home/project/workspace-cli/wrcli/wrk_build')
# this_path = '/home/project/workspace-cli/wrcli/wrk_build'
# conf_file = "/home/project/workspace-cli/tests/conf_parse/workspace-opt-field-miss-val.yaml"
# conf_dir_path = "/home/project/workspace-cli/tests/conf_parse/workspace-dirs/correct"
import logging
import json, yaml
from pathlib import Path
from distutils.dir_util import copy_tree
from .conf_parser import read_conf_dir
from ..globals import *


def init_wrk():
    """  ->> bool
    Check if this workspace has UI folder. If not copy the 
    boilerplate - the default starting UI
    """
    try:
        if not Path(WORKSPACE_DIR).is_dir():
            logging.info('Initiating workspace...')
            this_path = os.path.dirname(os.path.realpath(__file__))
            copy_tree(os.path.join(this_path, 'ui'), WORKSPACE_UI_DIR)
        else:
            logging.info('Workspace initialized')
    except:
        logging.critical("Something went wrong. Is workspace folder deleted?")
        return False
    return True











#### Start apps & logs

def generate_app_log_dir():
    """
    Create folder in /var/log/wrk-apps for this application
    """
    pass


def generate_app_start_command():
    """
    Generate supervisord file for the app to start
    """
    pass


def build_ui(conf_dir_path):
    """
    Rebuilds UI: icons, styles, fonts, pages
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






