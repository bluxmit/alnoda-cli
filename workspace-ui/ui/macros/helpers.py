"""
Basic example of a Mkdocs-macros module.
Include this  {{ macros_info() }} in any page to get complete macro info
"""
import os
import json
os.chdir("/home/project/workspace-utils/workspace-ui/ui")

def get_apps_dict():
    """ Read json with app UI dataforallpages
    """
    with open('conf/ui-apps.json') as json_file:
        apps_dict = json.load(json_file)
    return apps_dict


def get_url(app, port_increment):
    """ Get URL for every app. 
    Workspace can run on different ports or hosts.
    """
    app = app.upper()
    try:
        return os.environ[f"{app}_URL"]
    except:
        # Get host
        host = "localhost"
        try:
            host = os.environ["WRK_HOST"]
        except:
            pass
        proto = "http"
        try:
            proto = os.environ["WRK_PROTO"]
        except:
            pass
        # Entry port - port relative to which other ports will be calculated 
        entry_port = 8020
        try:
            entry_port = int(os.environ["ENTRY_PORT"])
        except:
            pass
        # Assign port
        try:
            port = port_increment + entry_port
        except:
            port = 80
        return f"{proto}://{host}:{port}"


# this function name should not be changed
def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """
    @env.macro
    def get_page_apps(page):
        # read page dict
        apps_dict = get_apps_dict()
        page_dict_raw = apps_dict[page]
        # enrich page dict with URLs
        page_dict = []
        for p,v in page_dict_raw.items():
            port_increment = v["id"]
            v['app_url'] = get_url(page, port_increment)
            page_dict.append(v)
        print(page_dict)
        return page_dict


            