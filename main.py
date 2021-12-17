import time

import requester
import json
import config

location_id_data = {}
exclude_ids = config.settings["loc_ids_to_exclude"]  # Gananoque & Tay Valley Old People One & Prescott


def parseLocationsToDict():
    # Locations.json is extracted from the bottom of the pomelo covid-vaccination "locations" html page where you select a spot.
    # Kinda stupid so I just extracted it and then saved it as a json.
    with open("data/locations.json", encoding="utf-8") as data_file:
        location_data = json.loads(data_file.read())["locations"]
    for location in location_data:
        loc_id = location["loc_id"]
        location_id_data[loc_id] = location


def locAddyToAddress(data):
    address = data["address"].strip()
    # address2 = data["address2"].strip()
    city = data["city"].strip()
    # province = data["province"].strip()
    # country = data["country"].strip()
    postal = data["postal"].strip()

    loc_address = address + ", " + city + ", " + postal
    return loc_address


def check_locations(checking_locations, verbose_output):
    config.resetLastAvailableDate()
    for x in checking_locations:
        if x["id"] not in exclude_ids:
            loc_id = x["id"]
            loc_name = location_id_data[loc_id]["loc_name"].replace("  ", " ")
            loc_address = locAddyToAddress(location_id_data[loc_id]["address"])
            unavailable = x["hasUnavailableAppointments"]

            if verbose_output:
                print(f"{loc_id} {loc_name} ({loc_address})")
                if unavailable:
                    print(f"{loc_id} No appointments available.")
                    print("*" * 50)

            if not unavailable:
                earliest_date = requester.findEarliestDate(loc_id)
                if earliest_date["available"]:
                    current_loc_data = earliest_date["nextByLocId"][0]

                    config_epoch = config.settings["earliest_epoch"]
                    next_epoch = current_loc_data["next_date"]
                    readable_time = current_loc_data["next"]

                    if config_epoch == 0 or next_epoch < config_epoch:
                        # Found new epoch!

                        value_list = [readable_time, next_epoch, loc_id, loc_name, loc_address]
                        key_list = ["earliest_date", "earliest_epoch", "earliest_loc_id", "earliest_loc_name",
                                    "earliest_loc_address"]

                        config.updateKeys(key_list, value_list)

                    if verbose_output:
                        print(f"{loc_id} {readable_time}")
                        print("*" * 50)


def alertAvailableDate():
    latest_epoch = config.settings["earliest_epoch"]
    alert_epoch = config.settings["alert_epoch"]
    last_epoch_alerted = config.settings["last_epoch_alerted"]

    date = config.settings["earliest_date"]
    loc_name = config.settings["earliest_loc_name"]
    loc_address = config.settings["earliest_loc_address"]
    if latest_epoch != 0 and last_epoch_alerted != latest_epoch:
        if latest_epoch < alert_epoch:
            # New Time is before alert epoch! Announce
            print("NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME ")
            print("NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME ")
            print("NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME NEW TIME ")
            print(f"{loc_name} ({loc_address})")
            print(f"ALERT NEW TIME: {date})")
            config.update("last_epoch_alerted", latest_epoch)
        else:
            # This will output every time a different earliest date is available.
            # Remove to only alert before the alert epoch
            print(f"{loc_name} ({loc_address})")
            print(f"AVAILABLE: {date}")
            config.update("last_epoch_alerted", latest_epoch)


if __name__ == "__main__":
    print("Pomelo Vaccination Appointment Date Scraper")
    print("*" * 50)
    parseLocationsToDict()

    #requester.getHMSession()
    active_locations = requester.getLocations()
    check_locations(active_locations, True)
    alertAvailableDate()
    print("*" * 50)
    time.sleep(60)
    for i in range(5000):
        active_locations = requester.getLocations()
        check_locations(active_locations, False)
        alertAvailableDate()
        print("*" * 50)
        time.sleep(60)
