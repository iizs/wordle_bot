import http.client
import json
import time


# main
ALPHABET = 'abcdefghijklmnopqrsltuvwxyz'
MIN_LENGTH = 5
MAX_LENGTH = 5
DATA_PATH = 'data'
DATA_FILE = '{}/scrabble.merriam.{}{:02d}.json'
API_URI = '/lapi/1/sbl_finder/get_limited_data?mode=wfd&type=begins&rack={}&len={}'
SLEEP_TIME = 1

for c in ALPHABET:
    for l in range(MIN_LENGTH, MAX_LENGTH+1):
        conn = http.client.HTTPSConnection("scrabble.merriam.com")
        out = DATA_FILE.format(DATA_PATH, c, l)
        url = API_URI.format(c, l)
        print('Getting {} {}'.format(c, l))
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            print('Error while fetching {}: {} {}'.format(url, response.status, response.reason))
            time.sleep(SLEEP_TIME)
            continue
        data_plain = response.read()
        data_json = json.loads(data_plain)
        with open(out, 'w') as f:
            json.dump(data_json, f)
        time.sleep(SLEEP_TIME)