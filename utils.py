import json
import os

def get_path(filename):
    return f'{os.getenv("DATA_PATH")}/{filename}'
