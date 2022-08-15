# coding: utf-8
from .drive_client import upload_file, download_file
from datetime import datetime

import os
import pickle
import pytz
import json
import uuid

FILE_PATH = os.path.abspath(os.environ['APP_CONFIG_PATH'])
TIMEZONE = pytz.timezone('America/Argentina/Buenos_Aires')

def save_backup(file_path):
    filename = 'app_config_{}.json'.format(datetime.now(TIMEZONE).isoformat())
    print("will save backup {}".format(filename))
    return upload_file(file_path, filename)

def load_backup(filename=None):
    print("will load backup {}".format(filename))
    return download_file(FILE_PATH, filename)

def do_config(data):
    print("will write new bot config", data)
    with open(FILE_PATH, 'w') as f:
        f.write(data)
    f.close()

def get_slots():
    print("will get slots")
    with open(FILE_PATH, 'r') as f:
        slots = json.load(f)
    f.close()
    print("loaded slots", slots)
    return slots

def process_slots(normalized_data):
    denormalized_tree = {}
    print('process_slots', normalized_data)
    denormalized_tree[normalized_data['name']] = {
        'slot_text': normalized_data['text'],
        'slot_options': map_slot_options(normalized_data['name'], normalized_data['children'], denormalized_tree) if len(normalized_data['children']) else []
    }
    return denormalized_tree

def map_slot_options(parent_id, children, denormalized_tree):
    slot_options = []
    for item in children:
        id = str(uuid.uuid4())
        slot_options.append({
            'slot_id': parent_id,
            'text': item['name'],
            'id': id
        })
        denormalized_tree[id] = {
            'slot_text': item['text'],
            'slot_options': map_slot_options(id, item['children'], denormalized_tree) if 'children' in item and len(item['children']) else []
        }
    return slot_options