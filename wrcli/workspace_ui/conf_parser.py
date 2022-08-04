"""
Simply parse configuration yaml file and validate inuts
"""
import logging
import os
# os.chdir('/home/project/workspace-cli/src/workspace-ui')
# conf_file = "/home/works/workspace.yaml"
from pathlib import Path
import yaml
from cerberus import Validator
schema = eval(open(Path(__file__).with_name('config_schema.py'), 'r').read())

REQUIRED_KEYS = {
    'name': 'Workspace requires name. Please add to the workspace.yaml a key "name"',
    'doc_url': 'Workspace must have documentation. Please add to the workspace.yaml a key "doc_url" with the link to the documentation URL',
    'about': 'Workspace needs a description. Please add to the workspace.yaml a key "about" with a short description', 
    }


def validate_main_required_keys_present(wrk_params):
    """ Validate presence of the required keys, raise exception of not found
    """
    for k, m in REQUIRED_KEYS.items():
        if k not in wrk_params.keys():
            raise Exception(m)
    return True


def validate_schema(wrk_params):
    """ Validate the config against the schema
    """
    v = Validator(schema)
    valid = v.validate(wrk_params)
    if not valid:
        raise Exception(v.errors)


def parse_config_file(conf_file):
    """ str -> {}
    :param conf_file: config yaml file path
    :returns: dict of workspace parameters, parsed from the config file
    :raises: exception if validator fails
    """
    with open(conf_file, 'r') as stream:
        wrk_params = yaml.safe_load(stream)

    validate_main_required_keys_present(wrk_params)
    
    
    
    










def process_page_config():
    pass


def process_configs():
    """
    """
    pass