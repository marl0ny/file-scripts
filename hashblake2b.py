#!/usr/bin/python3
"""
Take the BLAKE2b hash of every file inside a directory (excluding symlinks)
and dump it into a json file. This is to verify the integrity of the files
at a later date.
"""

import hashlib
import os
import json
import datetime
import argparse


def get_hash(file):
    """
    Get the hash of the file.
    """
    # Hashing a file:
    # https://stackoverflow.com/a/3431838
    # by quantumSoup (https://stackoverflow.com/users/370483)
    # question (https://stackoverflow.com/q/3431825)
    # by Alexander (https://stackoverflow.com/users/408168)
    hashable = hashlib.blake2b()
    with open(file, "rb") as f:
        for content in iter(lambda: f.read(2048), b''):
            hashable.update(content)
    return hashable.hexdigest()


def _dict_file_hashes(root_path, path, files):
    for f in os.scandir(path):
        if f.is_file():
            files[f.path.replace(root_path, './')] = get_hash(f.path)
        elif f.is_dir():
            _dict_file_hashes(root_path, f.path, files)


def dict_file_hashes(path):
    """
    Make a dictionary that maps each file containing the path
    to its hash.
    """
    path += '/' if path[-1] != '/' else ''
    files = {}
    _dict_file_hashes(path, path, files)
    return files


def get_date():
    """
    Return the current time and date in the format
    YY-MM-DD-HHMMSS in UTC time.
    """
    time = datetime.datetime.utcnow()
    year, month, day = time.year, time.month, time.day
    hour, minute, second =  time.hour, time.minute, time.second
    month = str(month) if month >= 10 else ("0{}".format(month))
    day = str(day) if day >= 10 else ("0{}".format(day))
    hour = str(hour) if hour >= 10 else ("0{}".format(hour))
    minute = str(minute) if minute >= 10 else ("0{}".format(minute))
    second = str(second) if second >= 10 else ("0{}".format(second))
    return "{}-{}-{}-{}{}{}".format(year, month, day,
                                    hour, minute, second)


parser = argparse.ArgumentParser(
    description='Record the BLAKE2b hash or every file '
                'in a directory and store this data in a json file.')
parser.add_argument('path', type=str, metavar='/path/to/directory', 
                    help='path to a directory')
args = parser.parse_args()
path = args.path
path = os.path.abspath(path)
files = dict_file_hashes(path)
json_data = {'path': path, 'files': files}
with open('hash-BLAKE2b_%s.json' % get_date(), 'w') as f:
    json.dump(json_data, f)
