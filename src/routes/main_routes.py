from flask import Blueprint, render_template, jsonify, current_app


class MainRoutes:
    def __init__(self, grid_strategy):
        self.grid_strategy = grid_strategy
        self.main_routes = Blueprint('main', __name__)  # Define the Blueprint

        # Register routes
        self.main_routes.add_url_rule('/', methods=['GET'], view_func=self.home)
        self.main_routes.add_url_rule('/routes', methods=['GET'], view_func=self.list_routes)
        self.main_routes.add_url_rule('/order_history', methods=['GET'], view_func=self.get_order_history)
        self.main_routes.add_url_rule('/realized_profit_loss', methods=['GET'], view_func=self.get_realized_profit_loss)
        self.main_routes.add_url_rule('/matched_profit', methods=['GET'], view_func=self.get_matched_profit)

    @staticmethod
    def home():
        return render_template('index.html')

    @staticmethod
    def list_routes():
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
            open_orders = self.grid_strategy.exchange.fetch_open_orders('ETH/USDT')

            # Fetch closed orders (order history) from the exchange
            closed_orders = self.grid_strategy.exchange.fetch_closed_orders('ETH/USDT')

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
