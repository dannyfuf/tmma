import json
import os

def save_distance_index(distance_index):
    # save dict as json
    distance_index_path = f'{os.getenv("DATA_PATH")}/distance_index.json'
    with open(distance_index_path, 'w') as f:
        json.dump(distance_index, f)
    print('saved distance index to: ', distance_index_path)

def load_distance_index():
    # load dict from json
    distance_index_path = f'{os.getenv("DATA_PATH")}/distance_index.json'
    with open(distance_index_path, 'r') as f:
        distance_index = json.load(f)
    print('loaded distance index from: ', distance_index_path)
    return distance_index