import pytest
from pathlib import Path
from wrcli.workspace_ui.conf_parser import validate_main_required_keys_present
import yaml

def read_test_connf(conf_file):
    fpath = Path(__file__).with_name(conf_file)
    print(fpath)
    with open(fpath, 'r') as stream:
        wrk_params = yaml.safe_load(stream)
    return wrk_params

def test_main_keys():
    wrk_params = read_test_connf('workspace-correct.yaml')
    assert validate_main_required_keys_present(wrk_params)