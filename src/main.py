import os

from src.exchange_manager import ExchangeManager
from src.routes.main_routes import MainRoutes
from flask import Flask

from src.strategy.grid_strategy import GridStrategy


def create_app():
    app = Flask(__name__)

    # Initialize exchange manager and grid strategy
    default__grid_strategy = GridStrategy(exchange_name=None, exchange_config=None, symbol=None,
                                          starting_price=None, grid_levels=None)  # use default grid strategy

    print("Creating instance of MainRoutes...")
    main_routes_instance = MainRoutes(default__grid_strategy)  # Create an instance of MainRoutes
    print("Registering the blueprint...")
    app.register_blueprint(main_routes_instance.main_routes)  # Register the blueprint

    return app


def main():
    try:
        print("Initializing project...")
        app = create_app()
        app.run(debug=True)

    except KeyboardInterrupt:
        print("\n\nTrading process interrupted by user. Exiting...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Ensure any necessary cleanup is done here
        print("Exiting program.")


if __name__ == "__main__":
    main()
