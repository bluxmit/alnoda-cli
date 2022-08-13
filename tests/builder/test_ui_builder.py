import pytest
from pytest import MonkeyPatch
from unittest.mock import patch
from pathlib import Path
from wrcli.wrk_build.conf_parser import *
from wrcli.wrk_build.ui_builder import *
import yaml
import os, shutil
from datetime import date
from ..conf_parse.test_config_dir import get_full_conf_dir_path


def mock_globals(monkeypatch, kdir="/tmp"):
    """
    """
    mgl = ["globals", "wrk_build.meta_about", "wrk_build.conf_parser", "wrk_build.ui_builder"]
    for m in mgl:
        try: monkeypatch.setattr(f"wrcli.{m}.HOME_DIR", f"{kdir}/")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.WORKSPACE_DIR", f"{kdir}/.wrk")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.WORKSPACE_UI_DIR", f"{kdir}/.wrk/ui")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.WORKSPACE_META_FILE", f"{kdir}/.wrk/meta.json")
        except: pass
    return


def test_init_wrk(monkeypatch):
    """ test that workspace is initiated in the proper folder """
    # MOCK
    mock_globals(monkeypatch)
    from wrcli.wrk_build import builder
    from wrcli.wrk_build.meta_about import read_meta 
    # TEST
    builder.init_wrk()
    # assert folder is initialized
    assert os.path.isdir("/tmp/.wrk"), "Workspace must be initialised"
    # assert meta refreshed with today's date
    m = read_meta()
    assert str(m['created']) == str(date.today()), "Meta should have today's date"
    # check subfolders and files were created
    assert os.path.isdir("/tmp/.wrk/ui"), "UI folder must be created"
    assert os.path.isdir("/tmp/.wrk/ui/conf"), "ui/conf folder must be created"
    assert os.path.isfile("/tmp/.wrk/ui/mkdocs.yml"), "mkdocs.yml must be copied"
    # clear test results
    shutil.rmtree("/tmp/.wrk")
    return


def test_wrk_build(monkeypatch):
    """ Integration test. Check that UI is properly buit from the config folder """
    # MOCK
    mock_globals(monkeypatch)
    from wrcli.wrk_build import builder
    from wrcli.wrk_build.meta_about import read_meta 
    # TEST
    # # Initialize
    builder.init_wrk()
    conf_dir_path = get_full_conf_dir_path("correct")
    # logging.debug(f"Testing wrk builds from path {conf_dir_path}")
    builder.build_workspace(conf_dir_path)



