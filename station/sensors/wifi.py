# station/sensors/wifi.py
import os
import subprocess

def get_wifi_signal_strength():
    """
    Get WiFi signal strength in dB.

    Returns:
        int: Signal strength in dB or None if an error occurs.
    """
    try:
        result = subprocess.check_output(["iwconfig", "wlan0"]).decode()
        signal_line = [line for line in result.splitlines() if "Signal level" in line]
        if signal_line:
            signal_db = int(signal_line[0].split("Signal level=")[-1].split()[0])
            return signal_db
    except Exception as e:
        print(f"Error reading WiFi signal strength: {e}")
        return None
