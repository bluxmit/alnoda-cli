import os
from pathlib import Path

HOME_DIR = Path.home()
WORKSPACE_DIR = os.path.join(HOME_DIR, '.wrk') 
WORKSPACE_UI_DIR = os.path.join(WORKSPACE_DIR, 'ui')

WORKSPACE_HOME_PAGES = ["home", "admin", "my_apps"]