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




URL = ['API_CREDZ']['API_URL']
res = req.get(URL)
json_data = res.json()
for dictionary in json_data['history']['observations']:
     # d contains all metrics except timestamp \n",
     d = dict(itertools.islice(dictionary.items(), 2, None))
     # Adding timestamp to metrics dict\n",
     # For UTC timestamp, pass dictionary['utcdate'] to get_timestamp()\n",
     d['timestamp'] = get_timestamp(dictionary['date'])
     # Convert to dataframe
     #print(d['timestamp'])
     #df = df.append(pd.Series(d), ignore_index=True)
#df.set_index('timestamp', inplace=True)
#print(d['tempi'])
test_session = requests.Session()
print str(int(time.time()))
for key in d:
    #payload = payload + "Fake_Meter_type=Meter_" + str(j) + " random_Float_value=" + str(temperature)+str(int(time.time()))
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
    #print(printStr)
    #print(key)
    #print(d[key])
'''
loaded_json = json.load(json_data)
for x in json_data:
	print("%s: %d" % (x, json_data[x]))

'''
'''
for data_field in json_data:
    print(data_field['version'])
'''

#print(json.dumps(res.json(), indent=2))

'''
res = req.get(URL)
json_data = res.json()
'''
'''
df = pd.DataFrame()
for dictionary in json_data['history']['observations']:
     # d contains all metrics except timestamp \n",
     d = dict(itertools.islice(dictionary.items(), 2, None))
     # Adding timestamp to metrics dict\n",
     # For UTC timestamp, pass dictionary['utcdate'] to get_timestamp()\n",
     d['timestamp'] = get_timestamp(dictionary['date'])
     # Convert to dataframe
     df = df.append(pd.Series(d), ignore_index=True)
df.set_index('timestamp', inplace=True)
'''
