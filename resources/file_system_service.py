import os
import json

def get_files(root_folder):
    arr = next(os.walk(root_folder))

    return_map = {
        'root' : arr[0],
        'folders' : arr[1],
        'files' : arr[2]
    }

    return json.dumps(return_map)
