import requests
import time
import hmac
import hashlib
from src import config


if __name__ == "__main__":
    api_key = config.API_KEY
    secret_key = config.API_SECRET

    base_url = 'https://testnet.binance.vision/api/v3/account'
    timestamp = int(time.time() * 1000)
    params = f'timestamp={timestamp}'
    signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()

    url = f"{base_url}?{params}&signature={signature}"
    headers = {'X-MBX-APIKEY': api_key}

    # Make the request
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        account_info = response.json()

        # Print the full account info
        print(account_info)

        # Print specific balance information
        balances = account_info.get('balances', [])
        for balance in balances:
            asset = balance.get('asset')
            free = balance.get('free')
            locked = balance.get('locked')
            print(f"Asset: {asset}, Free: {free}, Locked: {locked}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
