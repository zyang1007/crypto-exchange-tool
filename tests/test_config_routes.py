from src.routes.config_routes import ConfigRoutes
from flask import Flask


def create_app():
    app = Flask(__name__)

    # main_routes_instance = MainRoutes(default__grid_strategy)
    config_routes = ConfigRoutes()

    # app.register_blueprint(main_routes_instance.main_routes)
    app.register_blueprint(config_routes.config_routes)

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
