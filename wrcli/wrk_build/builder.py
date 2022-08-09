import os 
# os.chdir('/home/project/workspace-cli/wrcli/build')
# this_path = '/home/project/workspace-cli/wrcli/build'
# conf_file = "/home/project/workspace-cli/tests/conf_parse/workspace-opt-field-miss-val.yaml"
# conf_dir_path = "/home/project/workspace-cli/tests/conf_parse/workspace-dirs/correct"
import logging
import json, yaml
from pathlib import Path
from distutils.dir_util import copy_tree
from .conf_parser import read_conf_dir
from ..globals import WORKSPACE_DIR, WORKSPACE_HOME_PAGES


def init_wrk():
    """  ->> bool
    Check if this workspace has UI folder. If not copy the 
    boilerplate - the default starting UI
    """
    try:
        if not Path(WORKSPACE_DIR).is_dir():
            logging.info('Initiating workspace...')
            this_path = os.path.dirname(os.path.realpath(__file__))
            copy_tree(f"{this_path}/ui", f"{WORKSPACE_DIR}/ui")
        else:
            logging.info('Workspace initialized')
    except:
        logging.critical("Something went wrong. Is workspace folder deleted?")
        return False
    return True


def read_ui_conf():
    """ ->> {}
    Reads existing workspace UI json, and returns dict.

    :return: existing UI app configuration
    :rtype: dict
    """
    ui_dict = f"{WORKSPACE_DIR}/ui/conf/ui-apps.json"
    with open(ui_dict) as json_file:
        ui_apps = json.load(json_file)
    return ui_apps








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
    # Read config of existing UI
    ui_apps = read_ui_conf()
    # Read new user configs_dir
    wrk_params, files = read_conf_dir(conf_dir_path)






