from gpiozero import Button
from math import pi
from statistics import mean
from time import time, sleep

CM_IN_A_KM = 100000
SECS_IN_A_HOUR = 3600
ANEMOMETER_FACTOR = 1.18 # Adjustment for wind energy lost to friction

store_speeds = []
wind_speed_sensor = Button(5)
wind_count = 0 # Count of half rotations
start_time = time() # Time wind_count started
radius_cm = 9.0 # Radius from center to edge of anemometer cup
wind_interval = 5 # Interval in seconds to report wind speed

def reset_wind():
    """reset wind reading"""
    global wind_count, start_time
    wind_count = 0
    start_time = time()

def spin():
    """add 1 count every half rotation"""
    global wind_count
    wind_count = wind_count + 1
    # print("spin" + str(wind_count))

wind_speed_sensor.when_pressed = spin

def calculate_speed(time_sec):
    """calculate the speed for a given time period"""
    circumference_cm = (2 * pi) * radius_cm
    rotations = wind_count / 2.0
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_A_HOUR * ANEMOMETER_FACTOR

    return km_per_hour


while True:
    reset_wind()
    sleep(wind_interval)
    speed_this_interval = calculate_speed(time() - start_time)
    store_speeds.append(speed_this_interval)

    wind_gust = max(store_speeds)
    wind_speed = mean(store_speeds)
    print(wind_speed, wind_gust)
