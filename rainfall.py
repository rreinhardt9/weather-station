from gpiozero import Button
from time import sleep

BUCKET_CAPACITY = 0.2794 # mm

rain_sensor = Button(6)
tip_count = 0 # Count of bucket tips

def reset_rainfall():
    """reset rain reading"""
    global tip_count
    tip_count = 0

def tip():
    """record tip of rain bucket"""
    global tip_count
    tip_count += 1
    rain_mm = tip_count * BUCKET_CAPACITY
    print("Total rain (mm) " + str(rain_mm))

rain_sensor.when_pressed = tip

while True:
    1 + 1
    # sleep(1)
