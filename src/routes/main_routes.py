import json
import os

from flask import Blueprint, render_template, jsonify, request, current_app


class MainRoutes:
    def __init__(self, grid_strategy):
        self.grid_strategy = grid_strategy
        self.main_routes = Blueprint('main', __name__)  # Define the Blueprint

        # Register routes
        self.main_routes.add_url_rule('/config_grid', methods=['GET', 'PUT'], view_func=self.config_grid)
        self.main_routes.add_url_rule('/', methods=['GET'], view_func=self.home)
        self.main_routes.add_url_rule('/routes', methods=['GET'], view_func=self.list_routes)
        self.main_routes.add_url_rule('/order_history', methods=['GET'], view_func=self.get_order_history)
        self.main_routes.add_url_rule('/realized_profit_loss', methods=['GET'], view_func=self.get_realized_profit_loss)
        self.main_routes.add_url_rule('/matched_profit', methods=['GET'], view_func=self.get_matched_profit)

    @staticmethod
    def get_grid_config_path():
        # Construct the path to the config file
        base_path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(base_path, '../config/grid_config.json')
        return os.path.abspath(config_path)

    def read_grid_config(self):
        config_file_path = self.get_grid_config_path()
        print(f"Trying to read config from: {config_file_path}")  # Debugging line
        try:
            with open(config_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {config_file_path}")
            return None  # Handle error as needed

    def write_grid_config(self, data):
        config_file_path = self.get_grid_config_path()
        with open(config_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def config_grid(self):
        if request.method == 'PUT':
            new_config = request.json  # Get new config data from the request

            # Check if required parameters are present
            if not new_config:
                return jsonify({'error': 'No data provided'}), 400

            # Save the new configuration
            self.write_grid_config(new_config)
            return jsonify({'message': 'Grid configuration updated successfully', 'config': new_config}), 200

        # If GET request, load the current configuration
        if request.method == 'GET':
            config = self.read_grid_config()
            if config is None:
                return "Configuration file not found", 404
            return render_template('grid_config.html', config=config)

    def home(self):
        return render_template('index.html')

    def list_routes(self):
        routes = []
        for rule in current_app.url_map.iter_rules():
            routes.append((rule.endpoint, str(rule)))

        return render_template('list_routes.html', routes=routes)

    def get_order_history(self):
        """
        Fetch and display the order history, including open and closed orders, using the grid_strategy.
        """
        try:
            # Fetch open orders from the exchange via grid_strategy
            open_orders = self.grid_strategy.fetch_open_orders('ETH/USDT', 'futures')

            # Fetch closed orders (order history) from the exchange
            closed_orders = self.grid_strategy.fetch_closed_orders('ETH/USDT', 'futures')

            # Combine open and closed orders for display
            order_history_data = []

            for order in open_orders:
                order_history_data.append({
                    'id': order['id'],
                    'symbol': order['symbol'],
                    'amount': order['amount'],
                    'price': order['price'],
                    'side': order['side'],
                    'status': order['status'],
                    'date': order['datetime']
                })

            for order in closed_orders:
                order_history_data.append({
                    'id': order['id'],
                    'symbol': order['symbol'],
                    'amount': order['amount'],
                    'price': order['price'],
                    'status': order['status'],
                    'date': order['datetime']
                })

            # Render the template with combined open and closed orders data
            return render_template('order_history.html', orders=order_history_data)

        except Exception as e:
            # Handle and log any exceptions that occur during fetching
            print(f"Error fetching order history: {e}")
            return jsonify({'error': 'Failed to fetch order history.'}), 500

    def get_realized_profit_loss(self):
        # Example function call to get realized profit/loss
        realized_profit_loss = self.grid_strategy.compute_realized_profit_loss()
        return render_template('realized_profit_loss.html', profit_loss=realized_profit_loss)

    def get_matched_profit(self):
        matched_profits = self.grid_strategy.calculate_matched_profit()
        return render_template('matched_profit.html', matched_profits=matched_profits)
