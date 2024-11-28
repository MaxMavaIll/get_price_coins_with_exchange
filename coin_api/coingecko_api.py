import requests
import os
import json


class GeCoin_Api:

    def get_info_coins_list(self):
        url = f'{self.url}/coins/list'
        response = requests.get(url=url).json()
        self.set_coins_list(response)
    
    def preapare_to_request(self):
        tmp_str = ''

        for network, value in self.networks_info['networks'].items():
            if value is None:
                continue

            tmp_str += f'{value['id']},'

        return tmp_str

    def preapare_to_appsScript(self, price_coins):
        tmp_data = {}

        for network, value in self.networks_info['networks'].items(): 
            for network_price in price_coins:

                if value is None:
                    tmp_data[network] = None
                    continue
                elif network_price != value['id']:
                    continue
                
                tmp_data[network] = float(price_coins[network_price]['usd'])

        return tmp_data

    def get_info_networks(self):
        coins_list_data = self.get_coins_list()
        name_network_data = self.get_name_networks()
        data = { 'networks': {} }
        temp_data1 = { 'networks_not_working': [] }

        for network_name in name_network_data['networks']:
            temp_data = []
            name_symbol = network_name.split('|')
            name = name_symbol[0]
            symbol = None
            if len(name_symbol) == 2:
                symbol = name_symbol[1]
            

            for index, network_info in enumerate(coins_list_data):
                
                if name != network_info["name"]:
                    continue
                
                if symbol:
                    if symbol != network_info["symbol"]:
                        continue

                temp_data.append(coins_list_data[index])

            if temp_data == []:
                data['networks'][network_name] = None
                continue

            data['networks'][network_name] = temp_data[0]

        print(temp_data1)
        
        self.networks_info = data

    def request_price_coins(self):
        networks_ids = self.preapare_to_request()
        url = f'{self.url}/simple/price?ids={networks_ids}&vs_currencies=usd'

        response = requests.get(url=url)

        if response.status_code == 200:
            ready_for_appsScript = self.preapare_to_appsScript(response.json())
            return ready_for_appsScript

        else:
            print(f"Error requests to CoinGecko: status {response.status_code}\ntext error: {response.text}")


    def work_with_json(self, file_path: str, data: dict = None):
        if data is None:
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
                return {"status": "success", "message": "Data written successfully"}
        


    def get_name_networks(self):
       return self.work_with_json(self.name_networks_path)

    def set_name_networks(self, data: dict):
        self.work_with_json(self.name_networks_path, data)

    def get_coins_list(self):
       return self.work_with_json(self.coins_list_path)

    def set_coins_list(self, data: dict):
        self.work_with_json(self.coins_list_path, data)

    def __init__(self, 
                 url: str = None, 
                 name_networks_path: str = None,
                 coins_list_path: str = None,
            ):
        if url is None:
            url = 'https://api.coingecko.com/api/v3'
        
        if name_networks_path is None:
            name_networks_path_to_dir = os.path.abspath('data')
            name_networks_path = f"{name_networks_path_to_dir}/name_networks.json"
        
        if coins_list_path is None:
            coins_list_path = f"{name_networks_path_to_dir}/coins_list.json"

        self.url = url
        self.name_networks_path = name_networks_path
        self.coins_list_path = coins_list_path
        self.networks_ids = None
        self.networks_info = None

        if not os.path.isdir(name_networks_path_to_dir):
            os.mkdir(name_networks_path_to_dir)

        if not os.path.isfile(name_networks_path):
            print(self.work_with_json(name_networks_path, {}))

        if not os.path.isfile(coins_list_path):
            print(self.work_with_json(coins_list_path, {}))
        
