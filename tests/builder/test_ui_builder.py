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
        try: monkeypatch.setattr(f"wrcli.{m}.WORKSPACE_ABOUT_FILE", f"{kdir}/.wrk/ui/docs/about.md")
        except: pass  
        try: monkeypatch.setattr(f"wrcli.{m}.mkdocs_yml_path", f"{kdir}/.wrk/ui/mkdocs.yml")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.mkdocs_extra_css_path", f"{kdir}/.wrk/ui/docs/stylesheets/extra.css")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.mkdocs_assets_dir", f"{kdir}/.wrk/ui/docs/assets")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.ui_dict_file", f"{kdir}/.wrk/ui/conf/ui-apps.json")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.mkdocs_home_page_assets_dir", f"{kdir}/.wrk/ui/docs/assets")
        except: pass
        try: monkeypatch.setattr(f"wrcli.{m}.mkdocs_other_page_assets_dir", f"{kdir}/.wrk/ui/docs/pages")
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


def test_update_required_ui_params(monkeypatch):
    """ Test that updating of required UI parameters (parsed from the config.yaml)
    change the meta.json and about.md
    """
    # MOCK
    conf_dir_path = get_full_conf_dir_path("correct")
    name = 'This test workspace'; doc_url = 'http://this-test-link'; author = 'test-author'; version = 5.11; description = 'Test workspace description'
    wrk_params = {'name': name, 'doc_url': doc_url, 'author': author, 'version': version, 'description': description, 'logo': 'white-icon.svg', 'favicon': 'dark-icon.svg', 'styles': {'font': 'Roboto', 'colors': {'light': {'primary': '#252525', 'accent': '#19758F', 'background': '#F5F7F7'}, 'dark': {'primary': '#3C3C3C', 'accent': '#E77260', 'background': '#1E1E1E', 'title': '#9CDCFE', 'text': '#9CDCFE'}}, 'common_colors': {'header': '#FFFFFF', 'nav': '#eab676'}}} 
    mock_globals(monkeypatch)
    from wrcli.wrk_build import builder
    from wrcli.wrk_build.ui_builder import update_required_ui_params, get_mkdocs_yml
    from wrcli.wrk_build.meta_about import read_meta, read_about 
    # RUN TEST
    builder.init_wrk()
    update_required_ui_params(wrk_params, conf_dir_path)
    # CHECK mkdocs dict
    mkdocs_yml = get_mkdocs_yml()
    assert mkdocs_yml['site_name'] == name, f"The site_name in the mkdocs.yml file was not updated to {name}"
    ydoc = [d for d in mkdocs_yml['nav'] if 'Docs' in d.keys()][0]
    assert ydoc['Docs'] == doc_url, f"The doc url was not updated to {doc_url}"
    # CHECK meta
    meta = read_meta()
    assert meta['name'] == name, f"The name in meta.json was not updated to {name}"
    assert meta['version'] == version, f"The version in meta.json was not updated to {version}"
    assert meta['author'] == author, f"The author in meta.json was not updated to {author}"
    assert meta['description'] == description, f"The description in meta.json was not updated to {description}"
    # CHECK about
    about = read_about()
    assert name in about, f"workspace name {name} was not updated in the about.md"
    assert str(version) in about, f"version {version} was not updated in the about.md"
    assert author in about, f"author {author} was not updated in the about.md"
    assert description in about, f"description {description} was not updated in the about.md"
    # clear test results
    shutil.rmtree("/tmp/.wrk")
    return


def test_wrk_build(monkeypatch):
    """ Integration test. Check that UI is fully built from the config folder """
    # MOCK
    mock_globals(monkeypatch)
    from wrcli.wrk_build import builder
    from wrcli.wrk_build.meta_about import read_meta, read_about 
    # TEST
    # # Initialize
    builder.init_wrk()
    conf_dir_path = get_full_conf_dir_path("correct")
    # logging.debug(f"Testing wrk builds from path {conf_dir_path}")
    builder.build_workspace(conf_dir_path)
    #  
    #
    #
    # clear test results
    shutil.rmtree("/tmp/.wrk")
    return



