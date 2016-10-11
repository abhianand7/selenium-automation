import json
import logging
import os
import re


# this method will work as magic,
# give this method a search term and it will look into the whole json data to find something similar
def parse_json(json_object, search_term, depth=1, by_keys=True, by_values=False):

    pattern = re.compile(search_term)
    if by_keys and by_values:
        pass
    elif by_values:
        pass
    else:   # by default it will look by keys
        pass


def write_json(file_name='', *args):
    try:
        with open(file_name + '.json', 'w') as fobj:
            json.dump(args[0], fobj)
    except Exception as e:
        logging.warning('File write error: {}'.format(e))
    return None


def load_json(filename='', isfile=False, path=os.getcwd(), data=''):
    if isfile:
        try:
            with open(filename, 'r') as fobj:
                json_obj = json.load(fobj)
        except Exception as e:
            logging.warning('failed to fetch data from file: {}'.format(e))
            return None
        else:
            return json_obj
    else:
        try:
            json_obj = json.loads(data)
        except Exception as e:
            logging.warning('json decoding failed: {}'.format(e))
            return None
        else:
            return json_obj
