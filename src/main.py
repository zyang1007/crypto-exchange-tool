import json

from src.util.launcher import Launcher
from flask import Flask, render_template, request

app = Flask(__name__)


class Temp:  # temp class for testing with frontend and FLASK
    def __init__(self):
        self.count = None
        self.load_config()

    def load_config(self):
        """Load configuration from config.json."""
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.count = config['count']

    def update_config(self):
        """Update the configuration file."""
        with open('config.json', 'w') as f:
            json.dump({'count': self.count}, f)

    def decrement(self):
        if self.count > 0:
            self.count -= 1
            self.update_config()  # Save the updated count back to the config file

    def get_data(self):
        self.decrement()  # Decrement the count each time the route is called
        return render_template('get_data.html', price=self.count)

    def set_count(self, new_count):
        """Set a new value for count via a web form."""
        self.count = new_count
        self.update_config()  # Save to the config file


temp_instance = Temp()  # Creat a Temp instance


@app.route('/')  # Home page route
def home():
    return render_template('index.html')


# Register the route for the /data page with the instance method
app.add_url_rule('/get_data', view_func=temp_instance.get_data)


# Route for setting a new count value through a form
@app.route('/set_config', methods=['GET', 'POST'])
def set_config():
    if request.method == 'POST':
        new_count = int(request.form['count'])
        temp_instance.set_count(new_count)  # Update the count with the new value
        return f"New count value is set to: {new_count}"
    return render_template('set_config.html')  # Show the form to set a new count


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
