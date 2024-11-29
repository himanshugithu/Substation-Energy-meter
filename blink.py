import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 4  # Use GPIO 17 (adjust as per your connection)

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(LED_PIN, GPIO.OUT)

def blink():
    try:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        print("LED ON")
        time.sleep(0.5)  # Wait for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
        print("LED OFF")
        GPIO.cleanup()  # Reset GPIO settings
    except Exception as e:
        print(e)