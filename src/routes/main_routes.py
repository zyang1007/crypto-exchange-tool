# General routes
import json
import os

from flask import Blueprint, render_template, jsonify, current_app, request

main_routes = Blueprint('main', __name__)


# for frondend testing - connect to exchange using ccxt
import ccxt
exchange = ccxt.binance({
    'apiKey': '',
    'secret': '',
    'enableRateLimit': True, 
    'options': {
        'defaultType': 'spot',  
    },
})
exchange.set_sandbox_mode(True) 
symbol = 'ETH/USDT'
def get_market_ticker(symbol):
    ticker = exchange.fetch_ticker(symbol)
    # print(ticker)
    return ticker

##### ========================================================================

# functions to read/write/update grid_config.json
## Function to get path to config
def get_grid_config_path():
    # Construct the path to the config file
    base_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(base_path, '../config/grid_config.json')
    return os.path.abspath(config_path)  # Return the absolute path

## Function to read config
def read_grid_config():
    config_file_path = get_grid_config_path()
    print(f"Trying to read config from: {config_file_path}")  # Debugging line
    try:
        with open(config_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {config_file_path}")
        return None  # Handle error as needed

## Function to write/update config
def write_grid_config(data):
    config_file_path = get_grid_config_path()
    with open(config_file_path, 'w') as f:
        json.dump(data, f, indent=4)


##### ========================================================================

@main_routes.route('/config_grid', methods=['GET', 'PUT'])
def config_grid():
    if request.method == 'PUT':
        new_config = request.json  # Get new config data from the request

        # # Check if required parameters are present

        # Save the new configuration
        write_grid_config(new_config)
        return jsonify({'message': 'Grid configuration updated successfully', 'config': new_config})

    # If GET request, load the current configuration
    if request.method == 'GET':
        config = read_grid_config()
        if config is None:
            return "Configuration file not found", 404
        return jsonify(config)


@main_routes.route('/order_history', methods=['GET'])
def get_order_history():
    # Fetch order history from binance with ccxt
    # Below data is for demonstration purposes only, will use exchange instance to fetch real data.
    order_history_data = [
        {'id': 1, 'symbol': 'ETH/USDT', 'amount': 0.5, 'price': 2000, 'status': 'completed'},
        {'id': 2, 'symbol': 'ETH/USDT', 'amount': 1.0, 'price': 2500, 'status': 'completed'},
        {'id': 3, 'symbol': 'ETH/USDT', 'amount': 0.2, 'price': 2800, 'status': 'pending'},
    ]
    return jsonify(order_history_data)


@main_routes.route('/market_info', methods=['GET'])
def get_market_info():
    # Fetch market price from binance with ccxt
    market_info = get_market_ticker(symbol)["info"]
    return jsonify(market_info)


##### ========================================================================
# Homepage and List of routes


@main_routes.route('/')  # Define the /home route
def homepage():
    return current_app.send_static_file('home.html')


@main_routes.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append((rule.endpoint, str(rule)))
    return render_template('list_routes.html', routes=routes)

