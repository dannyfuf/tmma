import json
import os

def save_distance_index(distance_index):
    # save dict as json
    distance_index_path = get_path('distance_index.json')
    with open(distance_index_path, 'w') as f:
        json.dump(distance_index, f)
    print('saved distance index to: ', distance_index_path)

def load_distance_index(path):
    with open(path, 'r') as f:
        distance_index = json.load(f)
    print('loaded distance index from: ', path)
    return distance_index

def get_path(filename):
    return f'{os.getenv("DATA_PATH")}/{filename}'

def spaces_len(command):
    divider_len = 40
    return int(divider_len//2 - len(command)-2)

def log(message, data={}):
    log = {
        "message": message,
        "data": data
    }
    print(json.dumps(log, indent=4))
