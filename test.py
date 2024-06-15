import requests
import json

url = "http://localhost:8000/ask"
headers = {"Content-Type": "application/json"}
data = {"question": "sample question"}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Failed to get a valid response. Status code:", response.status_code)
    print("Response content:", response.text)
