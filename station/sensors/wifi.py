# station/sensors/wifi.py
import subprocess

def get_wifi_info():
    try:
        # Execute the iwconfig command
        result = subprocess.check_output(["iwconfig", "wlan0"]).decode()
        info = {}

        # Parse the output line by line
        for line in result.splitlines():
            if "ESSID" in line:
                info["ssid"] = line.split("ESSID:")[-1].strip().replace('"', "")
            if "Bit Rate" in line:
                info["bitrate"] = line.split("Bit Rate=")[-1].split()[0]
            if "Frequency" in line:
                info["frequency"] = line.split("Frequency:")[-1].split()[0]
            if "Signal level" in line:
                signal_part = line.split("Signal level=")[-1].split()[0]
                info["signal_db"] = int(signal_part) if signal_part.isdigit() else None

        return info
    except subprocess.CalledProcessError as e:
        print(f"Error fetching WiFi info: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}
