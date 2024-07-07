import json
import numpy as np

#* JSON Functions
def load_json(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
        data =  json.loads(data)

    return data

def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)