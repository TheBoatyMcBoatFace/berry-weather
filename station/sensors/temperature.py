# station/sensors/temperature.py
import os
import glob
import time

def setup_temperature_sensors(one_wire_pin):
    """
    Setup One-Wire temperature sensors.

    Args:
        one_wire_pin (str): GPIO pin configured for the One-Wire bus.
    Returns:
        list: A list of available sensor device paths.
    """
    base_dir = "/sys/bus/w1/devices/"
    devices = glob.glob(base_dir + "28-*")
    return [{"id": device.split('/')[-1], "path": device + "/w1_slave"} for device in devices]

def read_temp_raw(device_file):
    """Read raw data from the sensor."""
    with open(device_file, "r") as f:
        return f.readlines()

def read_temp(device_file):
    """
    Read and parse the temperature from a One-Wire sensor.
    Converts Celsius to Fahrenheit.
    """
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_c = float(lines[1][equals_pos + 2:]) / 1000.0
        return temp_c * 9.0 / 5.0 + 32.0

def get_temperatures(sensors):
    """
    Get temperature readings from configured sensors.

    Args:
        sensors (list): List of sensor configurations.
    Returns:
        dict: Dictionary of sensor IDs and their temperature readings.
    """
    readings = {}
    for sensor in sensors:
        try:
            readings[sensor["id"]] = read_temp(sensor["path"])
        except Exception as e:
            readings[sensor["id"]] = None
            print(f"Error reading sensor {sensor['id']}: {e}")
    return readings
