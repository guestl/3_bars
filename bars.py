import json
import codecs
import argparse
import os.path
from math import radians, cos, sin, asin, sqrt
import logging


def load_json_from_file(file_path):
    with codecs.open(file_path, 'r', 'utf8') as f:
        json_file_data = f.read()
    return json_file_data


def get_parsed_json(loaded_data):
    try:
        parsed_json_data = json.loads(loaded_data)
        return parsed_json_data['features']
    except ValueError:
        logging.error("Value error in json file")
        return None


def get_biggest_bar(bars_dict):
    return max(bars_dict,
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars_dict):
    return min(bars_dict,
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def haversine(lon1, lat1, lon2, lat2):
    # from https://stackoverflow.com/questions/4913349/

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a_koeff = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c_koeff = 2 * asin(sqrt(a_koeff))

    earth_radius = 6371  # in kilometers. Use 3956 for miles
    return c_koeff * earth_radius


def get_closest_bar(bars_list, longitude, latitude):
    distance_list = [([single_bar, haversine(
        single_bar['geometry']['coordinates'][0],
        single_bar['geometry']['coordinates'][1],
        longitude, latitude)]) for single_bar in bars_list]

    return min(distance_list, key=lambda x: x[1])[0]


def get_print_bar_string(single_bar, str_bar_property):
    return str_bar_property + " bar is {} located in {} and with {} seats".\
        format(single_bar['properties']['Attributes']['Name'],
               single_bar['properties']['Attributes']['Address'],
               single_bar['properties']['Attributes']['SeatsCount'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script look for\
             smallest, biggest and closest bar in Moscow.')
    parser.add_argument('json_filename', type=str,
                        help='JSON filename.')

    args = parser.parse_args()
    json_filename = args.json_filename

    if os.path.isfile(json_filename):
        loaded_data = load_json_from_file(json_filename)
    else:
        exit("Json file '{}' must exists".format(json_filename))

    parsed_json_dict = get_parsed_json(loaded_data)

    if not parsed_json_dict:
        exit()

    try:
        user_longitude = float(input("Enter your longitude:"))
        user_latitude = float(input("Enter your latitude:"))
    except ValueError:
        exit("Incorrect coordinates. \
            \nYou have to use only digits and dots")

    closest_bar = get_closest_bar(
        parsed_json_dict, user_latitude, user_longitude)

    print(get_print_bar_string(get_smallest_bar(parsed_json_dict), 'Smallest'))
    print(get_print_bar_string(get_biggest_bar(parsed_json_dict), 'Biggest'))
    print(get_print_bar_string(closest_bar, 'Closest'))
