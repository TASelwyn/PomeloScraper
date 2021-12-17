import json
import os

global settings

config_filepath = "data/config.json"


def readConfig():
    global settings

    with open(config_filepath, encoding="utf-8") as data_file:
        settings = json.loads(data_file.read())


def saveConfig():
    global settings

    with open(config_filepath, "w", encoding="utf-8") as data_file:
        json.dump(settings, data_file, indent=4)


def createConfig():
    global settings

    settings = {
        "earliest_date": "",
        "earliest_epoch": 0,
        "earliest_loc_id": 0,
        "earliest_loc_name": "",
        "earliest_loc_address": "",
        "alert_epoch": 1641269100,
        "last_epoch_alerted": 0,
        "loc_ids_to_exclude": [1405, 1501, 1663]
    }

    if not os.path.exists(os.path.dirname(config_filepath)):
        os.makedirs(os.path.dirname(config_filepath))

    saveConfig()


def updateKeys(key_list, new_value_list):
    # Use function so it auto saves the cache value
    for i in range(len(key_list)):
        settings[key_list[i]] = new_value_list[i]
    saveConfig()


def update(key, value):
    settings[key] = value
    saveConfig()


def resetLastAvailableDate():
    settings["earliest_date"] = ""
    settings["earliest_epoch"] = 0
    settings["earliest_loc_id"] = 0
    settings["earliest_loc_name"] = ""
    settings["earliest_loc_address"] = ""

    saveConfig()


# Load config into memory
if os.path.isfile(config_filepath):
    readConfig()
else:
    createConfig()
    readConfig()
