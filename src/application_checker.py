import json
import os


def check_file_path(app_name: str):
    with open("app_path.json", "r") as file:
        res = json.load(file)
        found = False
        for path in res['file_paths']:
            expand_path = os.path.expandvars(path['path'])  # used to expand %USERNAME% to the current user
            if path['name'] == app_name and os.path.exists(expand_path):
                print('app exists already')
                found = True
                return found
        if not found:
            print("could not locate file path")
            return False


check_file_path("Visual Studio Code")
