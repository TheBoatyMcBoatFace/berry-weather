# station/gpio/setup.py

import RPi.GPIO as GPIO

def setup_gpio():
    """
    Configure GPIO pins for the Raspberry Pi.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)  # Use GPIO4 for One-Wire
    return GPIO
