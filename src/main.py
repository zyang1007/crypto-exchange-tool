from src.routes.config_routes import ConfigRoutes
from src.routes.main_routes import MainRoutes
from flask import Flask

from src.service.exchange import Exchange
from src.strategy.grid_strategy import GridStrategy


def create_app():
    app = Flask(__name__)

    # Initialize exchange manager and grid strategy
    exchange = Exchange()
    default__grid_strategy = GridStrategy(exchange)  # use default grid strategy

    print("Creating instance of MainRoutes...")  # Create an instance of MainRoutes
    main_routes_instance = MainRoutes(default__grid_strategy)
    config_routes = ConfigRoutes()

    print("Registering the blueprints...")  # Register blueprints
    app.register_blueprint(main_routes_instance.main_routes)
    app.register_blueprint(config_routes.config_routes)

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
