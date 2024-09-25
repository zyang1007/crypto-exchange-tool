from src.routes.main_routes import main_routes
from flask import Flask

app = Flask(__name__,static_url_path='')
app.register_blueprint(main_routes, url_prefix='/')  # Optionally add a URL prefix


def main():
    try:
        config = {
            'apiKey': 'your-api-key',
            'secret': 'your-secret',
            'baseURL': 'https://testnet.binancefuture.com'
        }
        print("Initializing project...")
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
