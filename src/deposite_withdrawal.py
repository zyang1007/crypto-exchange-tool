import requests
import hmac
import hashlib
import time

# Replace with your actual Binance API key and secret
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_SECRET_KEY'

# Base URL for Binance's API
base_url = 'https://api.binance.com'
deposit_address_endpoint = '/sapi/v1/capital/deposit/address'
withdraw_endpoint = '/sapi/v1/capital/withdraw/apply'


def create_signature(params, secret):
    """
    Create HMAC SHA256 signature for Binance API requests.
    """
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()


def get_deposit_address(api_key, api_secret, asset):
    """
    Function to get the deposit address for a given asset.
    - asset: The asset for which you want to retrieve the deposit address (e.g., BTC, ETH)
    """
    params = {
        'asset': asset,  # e.g., 'BTC', 'ETH'
        'timestamp': int(time.time() * 1000),  # Timestamp in milliseconds
    }
    # Generate the signature required by the Binance API
    params['signature'] = create_signature(params, api_secret)
    headers = {
        'X-MBX-APIKEY': api_key,  # API key required in headers
    }
    # Send a GET request to the deposit address endpoint
    response = requests.get(base_url + deposit_address_endpoint, headers=headers, params=params)
    return response.json()  # Return the JSON response


def withdraw_funds(api_key, api_secret, asset, amount, address, address_tag=''):
    """
    Function to withdraw funds to a specified address.
    - asset: The asset to withdraw (e.g., BTC, ETH)
    - amount: The amount to withdraw
    - address: The withdrawal address
    - address_tag: Optional; required for certain assets (e.g., XRP, BNB)
    """
    params = {
        'asset': asset,  # e.g., 'BTC'
        'amount': amount,  # Amount to withdraw
        'address': address,  # Withdrawal address
        'addressTag': address_tag,  # Optional, for assets that require a tag
        'timestamp': int(time.time() * 1000),  # Timestamp in milliseconds
    }
    # Generate the signature required by the Binance API
    params['signature'] = create_signature(params, api_secret)
    headers = {
        'X-MBX-APIKEY': api_key,  # API key required in headers
    }
    # Send a POST request to the withdrawal endpoint
    response = requests.post(base_url + withdraw_endpoint, headers=headers, params=params)
    return response.json()  # Return the JSON response


# Example usage:

# Get deposit address for BTC
print("Fetching deposit address for BTC...")
deposit_address_result = get_deposit_address(api_key, api_secret, 'BTC')
print("Deposit Address:", deposit_address_result)

# Withdraw 0.1 BTC to a specified address
print("Initiating withdrawal of 0.1 BTC...")
withdraw_result = withdraw_funds(api_key, api_secret, 'BTC', 0.1, 'YOUR_WITHDRAWAL_ADDRESS')
print("Withdrawal Result:", withdraw_result)
