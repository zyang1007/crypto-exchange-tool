from flask import Flask

from src.routes.main_routes import MainRoutes
from src.service.exchange import Exchange


def create_app():
    app = Flask(__name__)
    exchange = Exchange
    # main_routes_instance = MainRoutes(default__grid_strategy)
    main_routes = MainRoutes(Exchange)

    # app.register_blueprint(main_routes_instance.main_routes)
    app.register_blueprint(main_routes.main_routes)

    return app


if __name__ == '__main__':

    try:
        print("Initializing Flask app...")
        app = create_app()
        app.run(debug=True)

    except KeyboardInterrupt:
        print("\n\nTrading process interrupted by user. Exiting...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Ensure any necessary cleanup is done here
        print("Exiting program.")
