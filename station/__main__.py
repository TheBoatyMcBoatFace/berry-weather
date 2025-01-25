# station/__main__.py
from flask import Flask, jsonify, render_template
from threading import Thread, Lock
import time
from .config import load_config
from .sensors import *
from .gpio import setup_gpio
import RPi.GPIO as GPIO
import signal
import sys

app = Flask(__name__)

# Shared state
data = {
    "temperatures": {},
    "wifi_info": {},
    "system_stats": {},
    "bme680": {"temperature": None, "humidity": None, "pressure": None, "gas_resistance": None},
}
config = None
data_lock = Lock()  # Ensure thread-safe access to shared state


def read_sensors():
    """Continuously read sensors and update shared state."""
    global data
    temperature_sensors = setup_temperature_sensors(config["one_wire"]["pin"])
    bme680_sensor = setup_bme680()

    while True:
        try:
            with data_lock:
                # Update temperature readings
                raw_temperatures = get_temperatures(temperature_sensors)
                data["temperatures"] = {
                    sensor["name"]: round(raw_temperatures.get(sensor["id"], None), 2)
                    for sensor in config["sensors"]["temperature"]
                }
                print(f"[LOG] Temperature readings updated: {data['temperatures']}")

                # Update WiFi info
                data["wifi_info"] = get_wifi_info()
                print(f"[LOG] WiFi info updated: {data['wifi_info']}")

                # Update system stats
                data["system_stats"] = get_system_stats()
                print(f"[LOG] System stats updated: {data['system_stats']}")

                # Update BME680 readings
                if bme680_sensor:
                    data["bme680"] = read_bme680_data(bme680_sensor)
                    print(f"[LOG] BME680 readings updated: {data['bme680']}")
                else:
                    data["bme680"] = {"temperature": None, "humidity": None, "pressure": None, "gas_resistance": None}

        except Exception as e:
            print(f"Error reading sensors: {e}")

        # Wait for the configured update interval
        time.sleep(config["sensors"].get("wifi", {}).get("update_interval", 60))
@app.route("/")
def index():
    """Display sensor data on a webpage."""
    with data_lock:
        return render_template("index.html", data=data)


@app.route("/api")
def api():
    """Return sensor data as JSON."""
    with data_lock:
        return jsonify(data)


def cleanup():
    """Cleanup resources on exit."""
    print("Cleaning up GPIO and exiting...")
    GPIO.cleanup()
    sys.exit(0)


def signal_handler(sig, frame):
    """Handle termination signals."""
    cleanup()


def main():
    global config
    try:
        print("Starting Berry Weather...")

        # Handle termination signals
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Load configuration
        config = load_config()

        # Setup GPIO
        gpio = setup_gpio()

        # Start the sensor reading thread
        Thread(target=read_sensors, daemon=True).start()

        # Start Flask web server
        app.run(host="0.0.0.0", port=config.get("webserver", {}).get("port", 6969))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
