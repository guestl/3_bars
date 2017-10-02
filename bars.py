import json
import codecs
import sys
import os.path
from math import radians, cos, sin, asin, sqrt


def load_json_from_file(file_path):
    if file_path:
        with codecs.open(file_path, 'r', 'utf8') as f:
            json_file_data = f.read()
    return json_file_data


def get_parsed_json(loaded_data):
    seats_сount_dict = dict()
    gps_dict = dict()
    pure_data = dict()

    try:
        parsed_json_data = json.loads(loaded_data)
    except Exception as e:
        print("Unexpected error in json file")
        return None, None, None

    for item in parsed_json_data['features']:
        seats_сount_dict[item['properties']['RowId']] = item['properties']['Attributes']['SeatsCount']

        gps_dict[item['properties']['RowId']] = item['geometry']['coordinates']

        pure_data[item['properties']['RowId']] = item['properties']['Attributes']

    return seats_сount_dict, gps_dict, pure_data


def get_biggest_bar(bars_dict):
    return max(bars_dict.items(), key=lambda x: x[1])[0]


def get_smallest_bar(bars_dict):
    return min(bars_dict.items(), key=lambda x: x[1])[0]


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    from https://stackoverflow.com/questions/4913349/
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_closest_bar(bars_gps_dict, longitude, latitude):
    distance_dict = dict()
    for key, gps_value in bars_gps_dict.items():
        distance_dict[key] = haversine(gps_value[0], gps_value[1], longitude, latitude)
    return min(distance_dict.items(), key=lambda x: x[1])[0]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You have to use json file name as parameters. \
               \nExample: python bars.py <path to json file>")
        exit()

    json_file_name = sys.argv[1]

    if os.path.isfile(json_file_name):
        loaded_data = load_json_from_file(json_file_name)
    else:
        print("Json file '%s' must exists" % json_file_name)
        exit()

    seats_сount_dict, gps_dict, pure_json_data = get_parsed_json(loaded_data)

    if seats_сount_dict is None:
        print("Something went wrong during json parsing.")
        exit()

    try:
        user_longitude = float(input("Enter your longitude\
         \n(for example: 1.234567890):"))
        user_latitude = float(input("Enter your latitude\
         \n(for example: 1.234567890):"))
    except Exception as e:
        print("Incorrect coordinates. \
            \nYou have to use only digits and dots")
        exit()

    smallest_bar_id = get_smallest_bar(seats_сount_dict)
    biggest_bar_id = get_biggest_bar(seats_сount_dict)
    closest_bar_id = get_closest_bar(gps_dict, user_latitude, user_longitude)

    print("Smallest bar is %s located in %s and with %s seats" % 
    (pure_json_data[smallest_bar_id]['Name'], pure_json_data[smallest_bar_id]['Address'],
    pure_json_data[smallest_bar_id]['SeatsCount']))

    print("Biggest bar is %s located in %s and with %s seats" % 
    (pure_json_data[biggest_bar_id]['Name'], pure_json_data[biggest_bar_id]['Address'],
    pure_json_data[biggest_bar_id]['SeatsCount']))

    print("Closest bar for user is %s located in %s and with %s seats" % 
    (pure_json_data[closest_bar_id]['Name'], pure_json_data[closest_bar_id]['Address'],
    pure_json_data[closest_bar_id]['SeatsCount']))
