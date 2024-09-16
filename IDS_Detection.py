import requests
import json
from datetime import datetime
import hashlib
import hmac
import base64

# Azure Monitor Workspace information
customer_id = '<Your Log Analytics Workspace ID>'
shared_key = '<Your Primary Key>'
log_type = 'CustomLog'

# Create the JSON object to send to Azure Monitor
data = json.dumps({
    "Time": datetime.utcnow().isoformat() + "Z",
    "Message": "Custom log entry from Python"
})

# Create the authorization signature
def build_signature(content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    string_to_hash = "{0}\n{1}\n{2}\n{3}\n{4}".format(method, str(content_length), content_type, x_headers, resource)
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    return "SharedKey {}:{}".format(customer_id, encoded_hash)

# Send the request
def post_data(customer_id, shared_key, body, log_type):
    method = "POST"
    content_type = "application/json"
    resource = "/api/logs"
    content_length = len(body)
    signature = build_signature(content_length, method, content_type, resource)
    uri = "https://" + customer_id + ".ods.opinsights.azure.com" + resource + "?api-version=2016-04-01"

    headers = {
        "content-type": content_type,
        "Authorization": signature,
        "Log-Type": log_type,
        "x-ms-date": datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    }

    response = requests.post(uri, data=body, headers=headers)
    if response.status_code >= 200 and response.status_code <= 299:
        print("Data successfully posted to Azure Monitor")
    else:
        print("Failed to post data. Response code: {}".format(response.status_code))

post_data(customer_id, shared_key, data, log_type)
