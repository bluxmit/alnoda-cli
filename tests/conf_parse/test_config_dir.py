import pytest
from pathlib import Path, PosixPath
from wrcli.workspace_ui.conf_parser import *
from tests.conf_parse.test_config_parser import read_test_conf
import yaml
import os



def get_full_conf_dir_path(conf_dir_path):
    dirpath = os.path.dirname(Path(__file__))
    fullpath = f"{dirpath}/workspace-dirs/{conf_dir_path}"
    return fullpath

def test_get_workspace_yaml():
    """ Test that workspace yaml file is found
    """
    files = [PosixPath('/home/works/IDE_copy.jpg'), PosixPath('/home/works/Htop.jpg'), PosixPath('/home/works/MC.jpg'), PosixPath('/home/works/workspace.yaml'), PosixPath('/home/works/Filebrowser.png'), PosixPath('/home/works/Cronicle.jpg')]
    yml_file = get_workspace_yaml(files)
    assert yml_file == PosixPath('/home/works/workspace.yaml')

def test_get_workspace_yml():
    """ Test that workspace yml file is found
    """
    files = [PosixPath('/home/works/IDE_copy.jpg'), PosixPath('/home/works/Htop.jpg'), PosixPath('/home/works/MC.jpg'), PosixPath('/home/works/workspace.yml'), PosixPath('/home/works/Filebrowser.png'), PosixPath('/home/works/Cronicle.jpg')]
    yml_file = get_workspace_yaml(files)
    assert yml_file == PosixPath('/home/works/workspace.yml')

def test_valid_image_extension():
    """ Check that only valid image extensions are allowed
    """
    assert valid_image_extension('/home/works/Htop.jpg'), "JPG image is allowed"
    assert valid_image_extension('/home/works/Htop.png'), "PNG image is allowed"
    assert valid_image_extension('/home/works/Htop.svg'), "SVG image is allowed"
    assert not valid_image_extension('/home/works/Htop.gif'), "GIF image is not allowed"

def test_get_ui_images():
    """ Check that gui images are selected
    """
    wrk_params = read_test_conf('workspace-correct.yaml')
    required_images = get_ui_images(wrk_params)
    assert required_images == ['white-icon.svg', 'dark-icon.svg', 'redis-commander.png', 'blast-radius.png', 'ara.png']

def test_proper_dir():
    """ Test the correct config folder
    """
    conf_dir_path = get_full_conf_dir_path("correct")
    print(conf_dir_path)
    assert read_conf_dir(conf_dir_path) is not None, "Should be the correct config dir"

def test_conf_dir_missing_image():
    """ Test the config folder with a missing image
    """
    conf_dir_path = get_full_conf_dir_path("missing-icon")
    print(conf_dir_path)
    assert read_conf_dir(conf_dir_path) is not None, "Should be the correct config dir"