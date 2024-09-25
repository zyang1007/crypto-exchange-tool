# General routes
import json
import os

from flask import Blueprint, render_template, jsonify, current_app, request

main_routes = Blueprint('main', __name__)


def get_grid_config_path():
    # Construct the path to the config file
    base_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(base_path, '../config/grid_config.json')
    return os.path.abspath(config_path)  # Return the absolute path


def read_grid_config():
    config_file_path = get_grid_config_path()
    print(f"Trying to read config from: {config_file_path}")  # Debugging line
    try:
        with open(config_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {config_file_path}")
        return None  # Handle error as needed


# Function to write/update config
def write_grid_config(data):
    config_file_path = get_grid_config_path()
    with open(config_file_path, 'w') as f:
        json.dump(data, f, indent=4)


@main_routes.route('/config_grid', methods=['GET', 'PUT'])
def config_grid():
    if request.method == 'PUT':
        new_config = request.json  # Get new config data from the request

        # Check if required parameters are present
        if not new_config:
            return jsonify({'error': 'No data provided'}), 400

        # Save the new configuration
        write_grid_config(new_config)
        return jsonify({'message': 'Grid configuration updated successfully', 'config': new_config}), 200

    # If GET request, load the current configuration
    if request.method == 'GET':
        config = read_grid_config()
        if config is None:
            return "Configuration file not found", 404
        return render_template('grid_config.html', config=config)


@main_routes.route('/')  # Define the /home route
def home():
    return render_template('index.html')  # Render the homepage


@main_routes.route('/get_data', methods=['GET'])
def get_data():
    # Logic to retrieve items
    return render_template('order_history.html')


@main_routes.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append((rule.endpoint, str(rule)))

    return render_template('list_routes.html', routes=routes)


@main_routes.route('/order_history', methods=['GET'])
def get_order_history():
    # Fetch order history from binance with ccxt
    # Below data is for demonstration purposes only, will use exchange instance to fetch real data.
    order_history_data = [
        {'id': 1, 'symbol': 'ETH/USDT', 'amount': 0.5, 'price': 2000, 'status': 'completed'},
        {'id': 2, 'symbol': 'ETH/USDT', 'amount': 1.0, 'price': 2500, 'status': 'completed'},
        {'id': 3, 'symbol': 'ETH/USDT', 'amount': 0.2, 'price': 2800, 'status': 'pending'},
    ]

    return render_template('order_history.html', orders=order_history_data)

