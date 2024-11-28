import requests
import json
import toml

config_toml = toml.load('config.toml')

URL = {
    "api_sheets": config_toml['gg_sheets']['url_sheets'],
}


def get_network() -> dict:
    params = {"action": "get_networks"}
    response = requests.get(URL["api_sheets"], params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error requests to Apps Script: status {response.status_code}\ntext error: {response.text}")

def update_price_google_sheets(data: dict):
    json_data = json.dumps(data)

    response = requests.post(URL["api_sheets"], data={'action': 'update_price', 'data': json_data})
    print(response.text)