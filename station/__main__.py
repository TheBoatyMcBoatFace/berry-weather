# station/__main__.py
from .config import load_config
from .sensors import setup_temperature_sensors, get_temperatures, get_wifi_signal_strength
from .gpio import setup_gpio
import RPi.GPIO as GPIO

def main():
    try:
        print("Starting Berry Weather...")
        config = load_config()

        # Setup GPIO
        gpio = setup_gpio()

        # Setup Sensors
        temperature_sensors = setup_temperature_sensors(config["one_wire"]["pin"])
        wifi_signal_strength = get_wifi_signal_strength()

        # Read Data
        temperatures = get_temperatures(temperature_sensors)
        print(f"Temperature readings: {temperatures}")
        print(f"WiFi Signal Strength: {wifi_signal_strength} dB")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

if __name__ == "__main__":
    main()
