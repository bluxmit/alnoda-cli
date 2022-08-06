"""
Basic example of a Mkdocs-macros module.
Include this  {{ macros_info() }} in any page to get complete macro info
"""
import os
import json


def get_apps_dict():
    """ -> {}
    Read json with app UI dataforallpages
    :return: applications configuration dict
    :rtype: dict
    """
    with open('conf/ui-apps.json') as json_file:
        apps_dict = json.load(json_file)
    return apps_dict


def get_quickstart_port():
    """ -> int
    Define the port for the Quickstart page
    :return: port for the workspace UI (Quickstart)
    :rtype: int
    """
    quickstart_port = 8020
    try:
        quickstart_port = int(os.environ["QUICKSTART_PORT"])
    except:
        pass
    return quickstart_port


def add_path(url, v):
    """ str, {} -> str
    If path is defined, add it to the URL
    """
    if "path" in v:
        if v["path"][0] == "/": path = v["path"][1:] 
        else: path = v["path"]
        url = f"{url}/{path}"
    return url


def get_url(app, v, quickstart_port):
    """ Get URL for every app. 
    Workspace can run on different ports or hosts.
    """
    app = app.upper()
    # Try to get the entire URL from the env variable
    try:
        url = os.environ[f"{app}_URL"]
        url = add_path(url, v)
        return url
    except:
        # Get host
        host = "localhost" # <- default host
        # Try to get host environment from the env variable
        try:
            host = os.environ["WRK_HOST"]
        except:
            pass
        proto = "http" # <- default protocol
        # Try to get protocol from environment from the env variable
        try:
            proto = os.environ["WRK_PROTO"] # <- i.e. https when self-hosted on cloud server
        except:
            pass
        # Entry port - port relative to which other ports will be calculated 
        port_increment = v['port'] - 8020
        # Assign port
        try:
            port = quickstart_port + port_increment
        except:
            port = 80
        # Construct URL
        url = f"{proto}://{host}:{port}"
        # If path is defined, add path too
        url = add_path(url, v)
        return url


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
        # get UI port (from environmental variable)
        quickstart_port = get_quickstart_port()
        # read page dict
        apps_dict = get_apps_dict()
        page_dict_raw = apps_dict[page]
        # enrich page dict with URLs
        page_dict = []
        for p,v in page_dict_raw.items():
            v['app_url'] = get_url(p, v, quickstart_port)
            page_dict.append(v)
        return page_dict


            