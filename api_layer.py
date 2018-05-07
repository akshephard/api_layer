import json
import time
import itertools
import requests as req
import requests
from datetime import datetime
import configparser


def get_timestamp(d):
    # Hardcoded seconds to \"00\" since the json does not contain \"seconds\" field
    return d['year'] + '-' + d['mon'] + '-' + d['mday'] + 'T' + d['hour'] + ':' + d['min'] + ':' + '00' + 'Z'
def get_timestamp_hourly(d):
    return d['year'] + '-' + d['mon_padded'] + '-' + d['mday_padded'] + 'T' + d['hour_padded'] + ':' + d['min'] + ':' + '00' + 'Z'
def get_metrics_hourly(d, name="english"):
    tmp = {}
    for key, value in d.items():
        if name in d[key]:
            tmp[key] = d[key][name]
        elif ('dir' in d[key]):
            tmp[key + '-dir'] = d[key]['dir']
            tmp[key + '-degrees'] = d[key]['degrees']
        else:
            tmp[key] = d[key]
    return tmp

send_url= 'http://localhost:8186/write'
params = {
    'db': 'pyTestDB'
}
headers = {
    'Content-Type': 'application/octet-stream',
    'Accept': 'text/plain'
}
method = 'POST'
config = configparser.ConfigParser()
config.read('/api_config_files/config.ini')




URL = config['API_CREDZ']['API_URL']
res = req.get(URL)
json_data = res.json()
for dictionary in json_data['history']['observations']:
     # d contains all metrics except timestamp \n",
     d = dict(itertools.islice(dictionary.items(), 2, None))
     # Adding timestamp to metrics dict\n",
     # For UTC timestamp, pass dictionary['utcdate'] to get_timestamp()\n",
     d['timestamp'] = get_timestamp(dictionary['date'])

test_session = requests.Session()
print str(int(time.time()))
for key in d:
    payload = "testDB " +str(key) +"=" + str(d[key]) + " " + str(int(time.time()))
    print(payload)
    response = test_session.request(
        method=method,
        url=send_url,
        params=params,
        data=payload,
        headers=headers,
        verify=True
    )
    print(response.text)
    print(response.status_code)
payload = "weather temperature=82 1465839830100400200"
print(payload)
response = test_session.request(
    method=method,
    url=send_url,
    params=params,
    data=payload,
    headers=headers,
    verify=True
    )
print(response.text)
print(response.status_code)
