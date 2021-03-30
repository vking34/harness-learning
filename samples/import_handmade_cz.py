"""
Import sample data for recommendation engine
"""

import argparse
import random
import datetime
import pytz
import requests

RATE_ACTIONS_DELIMITER = ","
PROPERTIES_DELIMITER = ":"
SEED = 1


def import_events(file, url):
    f = open(file, 'r')
    random.seed(SEED)
    count = 0
    # year, month, day[, hour[, minute[, second[
    #event_date = datetime.datetime(2015, 8, 13, 12, 24, 41)
    # - datetime.timedelta(days=2.7)
    now_date = datetime.datetime.now(pytz.utc)
    current_date = now_date
    event_time_increment = datetime.timedelta(days=-0.8)
    available_date_increment = datetime.timedelta(days=0.8)
    event_date = now_date - datetime.timedelta(days=2.4)
    available_date = event_date + datetime.timedelta(days=-2)
    expire_date = event_date + datetime.timedelta(days=2)
    print("Importing data...")

    for line in f:
        data = line.rstrip('\r\n').split(RATE_ACTIONS_DELIMITER)
        # For demonstration purpose action names are taken from input along with secondary actions on
        # For the UR add some item metadata

        if (data[1] != "$set"):
            resp = requests.post(url, json={
                'event': data[1],
                'entityType': 'user',
                'entityId': data[0],
                'targetEntityType': 'item',
                'targetEntityId': data[2],
                'eventTime': current_date.isoformat()
            })
            resp_data = resp.json()
            print(resp_data)

            print("Event: " + data[1] + " entity_id: " + data[0] + " target_entity_id: " + data[2] +
                  " current_date: " + current_date.isoformat())
        elif (data[1] == "$set"):  # must be a set event
            properties = data[2].split(PROPERTIES_DELIMITER)
            prop_name = properties.pop(0)
            prop_value = properties if not prop_name == 'defaultRank' else float(
                properties[0])
            event = {
                'event': data[1],
                'entityType': 'item',
                'entityId': data[0],
                'eventTime': current_date.isoformat(),
                'properties': {prop_name: prop_value}
            }

            resp = requests.post(url, json=event)
            resp_data = resp.json()
            print(resp_data)
            print("Event: " + data[1] + " entity_id: " + data[0] + " properties/"+prop_name+": " + str(properties) +
                  " current_date: " + current_date.isoformat())
        count += 1
        current_date += event_time_increment

    # items = ['Iphone 6', 'Ipad-retina', 'Nexus',
    #          'Surface', 'Iphone 4', 'Galaxy', 'Iphone 5']
    items = ['1796', '1795', '1794',
             '1793', '1792', '1791', '1797', '1789', '1788', '1787']
    print("All items: " + str(items))
    for item in items:
        resp = requests.post(url, json={
            'event': '$set',
            'entityType': 'item',
            'entityId': item,
            'eventTime': now_date.isoformat(),
            'properties': {
                "expires": expire_date.isoformat(),
                "available": available_date.isoformat(),
                "date": event_date.isoformat()
            }
        })
        resp_data = resp.json()
        print('item resp:', resp_data)
        print("Event: $set entity_id: " + item +
              " properties/availableDate: " + available_date.isoformat() +
              " properties/date: " + event_date.isoformat() +
              " properties/expireDate: " + expire_date.isoformat())
        expire_date += available_date_increment
        event_date += available_date_increment
        available_date += available_date_increment
        count += 1

    f.close()
    print("%s events are imported." % count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Import sample data for recommendation engine")
    parser.add_argument('--access_key', default='invald_access_key')
    parser.add_argument(
        '--url', default="http://localhost:9090/engines/2/events")
    parser.add_argument('--file', default="./sample-handmade-data.txt")

    args = parser.parse_args()

    # current = datetime.datetime.now(pytz.utc).isoformat()
    # print(current)
    # resp = requests.post(args.url, json={
    #             'event': 'purchase',
    #             'entityType': 'user',
    #             'entityId': 'u2',
    #             'targetEntityType': 'item',
    #             'targetEntityId': 'Iphone 6',
    #             'eventTime': current
    #         })

    # resp_data = resp.json()
    # print(resp_data)

    import_events(args.file, args.url)
