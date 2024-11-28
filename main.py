import toml
from datetime import datetime

from coin_api.coingecko_api import GeCoin_Api
from google_sheetsAPI import sheets


def main():
    curent_time = datetime.now()
    coins_gecko = GeCoin_Api()

    if curent_time.hour == 0:
        coins_gecko.set_name_networks(sheets.get_network())
        coins_gecko.get_info_coins_list()
    coins_gecko.get_info_networks()
    data = coins_gecko.request_price_coins()
    sheets.update_price_google_sheets(data)

    



if __name__ == "__main__":
    main()