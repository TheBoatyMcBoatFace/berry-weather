# station/sensors/bme680.py
import board
import busio
import adafruit_bme680

def setup_bme680():
    """
    Setup the BME680 sensor over I2C.
    Returns:
        bme680: Configured BME680 sensor object.
    """
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

        # Configure sensor options
        bme680.sea_level_pressure = 1013.25  # Adjust based on local sea level pressure
        return bme680
    except Exception as e:
        print(f"Error setting up BME680: {e}")
        return None


def read_bme680_data(sensor):
    """
    Read data from the BME680 sensor.
    Args:
        sensor (bme680): Configured BME680 sensor object.
    Returns:
        dict: Dictionary containing temperature, humidity, pressure, and gas resistance.
    """
    try:
        return {
            "temperature": round(sensor.temperature * 9 / 5 + 32, 2),  # Convert to Fahrenheit
            "humidity": round(sensor.humidity, 2),
            "pressure": round(sensor.pressure, 2),
            "gas_resistance": round(sensor.gas, 2)
        }
    except Exception as e:
        print(f"Error reading BME680 data: {e}")
        return {}
