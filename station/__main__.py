# station/__main__.py
from flask import Flask, jsonify, render_template
from threading import Thread
import time
from .config import load_config
from .sensors import setup_temperature_sensors, get_temperatures, get_wifi_signal_strength
from .gpio import setup_gpio
import RPi.GPIO as GPIO

app = Flask(__name__)

# Shared state
data = {"temperatures": {}, "wifi_signal": None}
config = None


def read_sensors():
    """Continuously read sensors and update shared state."""
    global data
    temperature_sensors = setup_temperature_sensors(config["one_wire"]["pin"])
    while True:
        try:
            # Update temperature readings
            raw_temperatures = get_temperatures(temperature_sensors)
            data["temperatures"] = {
                sensor["name"]: raw_temperatures.get(sensor["id"], None)
                for sensor in config["sensors"]["temperature"]
            }

            # Update WiFi signal strength
            data["wifi_signal"] = get_wifi_signal_strength()

        except Exception as e:
            print(f"Error reading sensors: {e}")

        # Wait for the configured update interval
        time.sleep(config["sensors"].get("wifi", {}).get("update_interval", 60))


@app.route("/")
def index():
    """Display sensor data on a webpage."""
    return render_template("index.html", data=data)


def main():
    global config
    try:
        print("Starting Berry Weather...")

        # Load configuration
        config = load_config()

        # Setup GPIO
        gpio = setup_gpio()

        # Start the sensor reading thread
        Thread(target=read_sensors, daemon=True).start()

        # Start Flask web server
        app.run(host="0.0.0.0", port=6969)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
