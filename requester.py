import requests
import config

# Every function in this file has to directly make it's own web request.

XSRF_TOKEN = "PLEASE_ENTER_YOUR_TOKEN_HERE"
HM_SESSION = "PLEASE_ENTER_YOUR_TOKEN_HERE"


def getHMSession():
    global HM_SESSION, XSRF_TOKEN

    # Was gonna fix this, but doesn't really matter tbh.
    # XSRF_TOKEN/HM_SESSION from a "locations" api request can last seemingly forever. The tokens from a normal guest call, might have to be passed through a few diff calls to get a long lasting session code.
    #

    headers = {
        'authority': 'portal.healthmyself.net',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_ga=GA1.2.474564274.1639692232; _gid=GA1.2.1183195401.1639692232; XSRF-TOKEN=; hm_session=; locale=; io=',
    }

    response = requests.get('https://portal.healthmyself.net/northgrenvillecovid19assessmentcentre/guest/',
                            headers=headers)
    data = response.headers['Set-Cookie'].split(" ")
    for x in data:
        print(data)
        if x[:10] == "hm_session":
            HM_SESSION = x[11:].replace(";", "")
            print(HM_SESSION)
            return HM_SESSION


def getLocations():
    locations_url = "https://portal.healthmyself.net/northgrenvillecovid19assessmentcentre/guest/booking/type/4515/locations"

    headers = {
        'authority': 'portal.healthmyself.net',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': f'XSRF-TOKEN={XSRF_TOKEN}; hm_session={HM_SESSION};'
    }

    response = requests.get(locations_url, headers=headers)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(response.content)
        return {}


def findEarliestDate(loc_id):
    schedule_url = "https://portal.healthmyself.net/northgrenvillecovid19assessmentcentre/guest/booking/4515/schedules"

    headers = {
        'authority': 'portal.healthmyself.net',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'x-socket-id': 'WjZ8dP-1Ea8b5ecuAK0h',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'x-hm-client-timezone': 'America/Toronto',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://portal.healthmyself.net/northgrenvillecovid19assessmentcentre/guest/',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': f'XSRF-TOKEN={XSRF_TOKEN}; hm_session={HM_SESSION};'
    }

    params = (
        ('locId', loc_id),
    )

    response = requests.get(schedule_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["data"][0]
    else:
        print(response.status_code, response)
        return {}
