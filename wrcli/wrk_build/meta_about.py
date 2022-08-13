"""
Module with functions to manage metsa.json and 'Abuot' 
tab in the workspace UI
"""
import os 
# os.chdir('/home/project/workspace-cli/wrcli/wrk_build')
# this_path = '/home/project/workspace-cli/wrcli/wrk_build'
# conf_file = "/home/project/workspace-cli/tests/conf_parse/workspace-opt-field-miss-val.yaml"
# conf_dir_path = "/home/project/workspace-cli/tests/conf_parse/workspace-dirs/correct"
import logging
import json, yaml
from pathlib import Path
from distutils.dir_util import copy_tree
from datetime import date
from .conf_parser import read_conf_dir
from jinja2 import Template
from ..globals import *
from .templates import about_page_template

WORKSPACE_ABOUT_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'about.md')


def read_meta():
    """ ->> {}
    Reads existing workspace UI json, and returns dict.

    :return: dict with workspace meta data
    :rtype: dict
    """
    with open(WORKSPACE_META_FILE) as json_file:
        ui_apps = json.load(json_file)
    return ui_apps


def write_meta(meta_dict):
    """ {} ->> 
    Overwrite existing workspace meta data json with the updated dict

    :param meta_dict: dict with the updated meta
    :type meta_dict: dict
    """
    with open(WORKSPACE_META_FILE, 'w') as file:
        json.dump(meta_dict, file, indent=4 * ' ')
    return 


def read_about():
    """ ->> str, str
    Reads MkDocs about.md file, strips out the header template
    and returns only the text from the About section

    :return: header section of the About page
    :rtype: str
    :return: description section of the About page
    :rtype: str
    """
    with open(WORKSPACE_ABOUT_FILE) as f:
        about_raw = f.read()
    return about


def write_about(about):
    """ str ->> 
    Only updates the "Description" section, leaving header the same

    :param about: new content for the 'About' page
    :type about: str
    """
    with open(WORKSPACE_ABOUT_FILE, 'w') as f:
        f.write(about)
    return


def update_meta(name=None, version=None, author=None, description=None):
    """ str, str, str, str ->> 
    Updates meta.json. When called without any args, it will 
    update 'created' field only. 

    :param name: workspace name
    :type name: str
    :param version: workspace version
    :type version: str
    :param author: workspace author
    :type author: str
    :param description: workspace description
    :type description: str
    """
    meta_dict = read_meta()
    if name is not None:
        meta_dict['name'] = name
    if version is not None:
        meta_dict['version'] = version
    if author is not None:
        meta_dict['author'] = author
    if description is not None:
        meta_dict['description'] = description
    meta_dict['created'] = str(date.today())
    write_meta(meta_dict)
    return


def refresh_about_from_meta():
    """  ->>
    Read meta.json, use its values for the about_page_template,
    and overwrite the about.md page
    """
    meta_dict = read_meta()
    tm = Template(about_page_template)
    new_about = tm.render(meta_dict)
    write_about(new_about)