""" 
Collection of fucntions to build and update the workspace UI 
in the orkspace folder. Update pages, styles, images, logos etc.
"""
import os 
import shutil
import sass
# os.chdir('/home/project/workspace-cli/wrcli/build')
# this_path = '/home/project/workspace-cli/wrcli/build'
# conf_file = "/home/project/workspace-cli/tests/conf_parse/workspace-opt-field-miss-val.yaml"
# conf_dir_path = "/home/project/workspace-cli/tests/conf_parse/workspace-dirs/correct"
import logging
import json, yaml
from pathlib import Path
from jinja2 import Template
from distutils.dir_util import copy_tree
from ..globals import WORKSPACE_DIR, WORKSPACE_HOME_PAGES
from .ui_styles import styles_str

mkdocs_yml_path = os.path.join(WORKSPACE_UI_DIR, 'mkdocs.yml') 
mkdocs_extra_css_path = os.path.join(WORKSPACE_UI_DIR, 'docs', 'stylesheets', 'extra.css') 
mkdocs_assets_dir = os.path.join(WORKSPACE_UI_DIR, 'docs', 'assets')
mkdocs_about_md_file = os.path.join(WORKSPACE_UI_DIR, 'docs', 'about.md')


def get_mkdocs_yml():
    """  ->> {}
    Reads mkdocs.yml from the workspace UI, and returns as dict

    :return: workspace mkdocs.yml as a dict
    :rtype: dict
    """
    with open(mkdocs_yml_path, 'r') as stream:
        mkdocs_dict = yaml.safe_load(stream)
    return mkdocs_dict


def update_mkdocs_yml(mkdocs_dict):
    """ {} ->> 
    Updates (replaces) mkdocs.yml with the new dict

    :param mkdocs_dict: dict with main configuration for MkDocs
    :type wrk_params: dict
    """
    with open(mkdocs_yml_path, 'w') as file:
        documents = yaml.dump(mkdocs_dict, file, default_flow_style=False)
    return


def update_required_ui_params(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update required ui parameters, such as workspace name

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    # Extract required workspace parameters
    name = wrk_params["name"]
    doc_url = wrk_params["doc_url"]
    about = wrk_params["about"]
    # Fetch existing mkdocs.yml file, make updates and save back
    # name
    mkdocs_dict = get_mkdocs_yml()
    mkdocs_dict["site_name"] = name
    # docs link
    for p in mkdocs_dict["nav"]:
        if 'Docs' in p.keys(): p['Docs'] = doc_url
    update_mkdocs_yml(mkdocs_dict)  # <- update mkdocs.yml now
    # about page
    with open(mkdocs_about_md_file, "w") as md_file:
        md_file.write(about)
    return


def update_optional_ui_params(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update optional ui parameters, such as workspace home page font

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    # Extract optional workspace parameters
    ## font
    if 'styles' in wrk_params and 'font' in wrk_params['styles']:
        mkdocs_dict = get_mkdocs_yml()
        if 'font' not in mkdocs_dict['theme']: 
            mkdocs_dict['theme']['font'] = {}
        mkdocs_dict['theme']['font']['text'] = wrk_params['styles']['font']
        update_mkdocs_yml(mkdocs_dict)
    return


def update_logo(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update existing workspace UI - change logo icon. 
    It checks whether new logo is defined in the wrk_params.
    If yes, uploads the logo file to the respective UI folder, and changes the mkdocs.yml file 

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    if 'logo' in wrk_params:
        # Update mkdocs.yml
        mkdocs_dict = get_mkdocs_yml()
        mkdocs_dict['theme']['logo'] = os.path.join('assets', wrk_params["logo"])
        update_mkdocs_yml(mkdocs_dict)
        # Copy file
        logo_file = os.path.join(conf_dir_path, wrk_params["logo"])
        shutil.copy2(logo_file, mkdocs_assets_dir)
        logging.debug(f"logo updated from file {logo_file}")
    return


def update_favicon(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update existing workspace UI - change favicon. 
    It checks whether new favicon is defined in the wrk_params.
    If yes, uploads the favicon file to the respective UI folder, and changes the mkdocs.yml file

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    if 'favicon' in wrk_params:
        # Update mkdocs.yml
        mkdocs_dict = get_mkdocs_yml()
        mkdocs_dict['theme']['favicon'] = os.path.join('assets', wrk_params["favicon"])
        update_mkdocs_yml(mkdocs_dict)
        # Copy file
        favicon_file = os.path.join(conf_dir_path, wrk_params["favicon"])
        shutil.copy2(favicon_file, mkdocs_assets_dir)
        logging.debug(f"favicon updated from file {favicon_file}")
    return


def update_ui_styles(wrk_params):
    """ {} ->> 
    Update existing workspace UI - change CSS styles

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    """
    # create dict with style settings
    d_styles = {}
    if 'styles' in wrk_params:
        if 'colors' in wrk_params['styles']:
            d_styles.update(wrk_params['styles']['colors'])
        if 'common_colors' in wrk_params['styles']:
            d_styles.update({'common_colors': wrk_params['styles']['common_colors']})
    if len(styles.keys()) > 0:      
        # generate jinja template
        tm = Template(styles_str)
        new_styles = tm.render({'styles': d_styles})
        # save styles to mkdocs stylesheet
        with open(mkdocs_extra_css_path, "w") as styles_file:
            styles_file.write(new_styles)
    return


def update_home_page(ui_apps, wrk_params):
    """ {}, str ->> 
    Update the Home page, if additional apps were added to this page

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    pass


def move_page_assets():
    """
    Copy respective assets (images) to the UI folder from the user's config dir
    """
    pass


def read_ui_conf():
    """ ->> {}
    Reads existing workspace UI json, and returns dict.

    :return: existing UI app configuration
    :rtype: dict
    """
    ui_dict = os.path.join(WORKSPACE_UI_DIR, 'conf', 'ui-apps.json')
    with open(ui_dict) as json_file:
        ui_apps = json.load(json_file)
    return ui_apps


def build_wrk_ui(wrk_params, conf_dir_path):
    """
    Gets existing UI config and the new user's config. And builds the new UI config,
    which is saved to the workspace UI folder
    """
    update_required_ui_params(wrk_params, conf_dir_path)
    update_optional_ui_params(wrk_params, conf_dir_path)
    update_logo(wrk_params, conf_dir_path)
    update_favicon(wrk_params, conf_dir_path)




