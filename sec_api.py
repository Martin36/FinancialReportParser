# package used to execute HTTP POST request to the API
import json
import urllib.request
import pprint

pp = pprint.PrettyPrinter(indent=2)

# API Key
TOKEN = "4990f657720f57e9abcbd388da4dd531b53dba8ee43907a9d6893199c6a6df9f" # replace YOUR_API_KEY with the API key you got from sec-api.io after sign up
# API endpoint
API_URL = "https://api.sec-api.io?token=" + TOKEN

# define the filter parameters you want to send to the API 
payload = {
  "query": { "query_string": { "query": "cik:320193 AND filedAt:{2020-07-01 TO 2021-03-31} AND formType:\"10-K\"" } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

# format your payload to JSON bytes
jsondata = json.dumps(payload)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

# instantiate the request 
req = urllib.request.Request(API_URL)

# set the correct HTTP header: Content-Type = application/json
req.add_header('Content-Type', 'application/json; charset=utf-8')
# set the correct length of your request
req.add_header('Content-Length', len(jsondataasbytes))

# send the request to the API
response = urllib.request.urlopen(req, jsondataasbytes)

# read the response 
res_body = response.read()
# transform the response into JSON
filings = json.loads(res_body.decode("utf-8"))

# print JSON 
pp.pprint(filings)