import requests
import hmac
import hashlib
import time

# Replace with actual Binance API key and secret
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_SECRET_KEY'

base_url = 'https://api.binance.com'  # Base URL for Binance's API
transfer_endpoint = '/sapi/v1/futures/transfer'


# This function creates an HMAC SHA256 signature based on the query parameters
def create_signature(params, secret):
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()


def transfer_funds(api_key, api_secret, asset, amount, type):
    """
    Function to transfer funds between spot and futures accounts.
    type:
    1 -> Transfer from Spot to Futures
    2 -> Transfer from Futures to Spot
    """
    params = {
        'asset': asset,  # e.g. 'ETH'
        'amount': amount,  # The amount to transfer
        'type': type,  # 1 for spot to futures, 2 for futures to spot
        'timestamp': int(time.time() * 1000),  # Timestamp in milliseconds
    }
    # Generate the signature required by the Binance API
    params['signature'] = create_signature(params, api_secret)
    headers = {
        'X-MBX-APIKEY': api_key,  # API key required in headers
    }
    # Send a POST request to the Binance transfer endpoint
    response = requests.post(base_url + transfer_endpoint, headers=headers, params=params)
    return response.json()  # Return the JSON response


# Example: Transfer 0.1 BTC from Spot to Futures
result = transfer_funds(api_key, api_secret, 'BTC', 0.1, 1)
print(result)
