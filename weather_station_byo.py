from gpiozero import Button
from math import pi
from statistics import mean
from time import time, sleep
# import bme280_sensor
import wind_direction_byo
import ds18b20_therm

CM_IN_A_KM = 100000
SECS_IN_A_HOUR = 3600
ANEMOMETER_FACTOR = 1.18 # Adjustment for wind energy lost to friction
BUCKET_CAPACITY = 0.2794 # mm

store_speeds = []
store_directions = []
tip_count = 0 # Count of rain bucket tips
wind_count = 0 # Count of half rotations
wind_observation_start_time = time() # Time wind_count started
radius_cm = 9.0 # Radius from center to edge of anemometer cup
wind_interval = 5 # Interval in seconds to take measurements
recording_interval = 30 # Interval in seconds to record measurements
wind_speed_sensor = Button(5)
rain_sensor = Button(6)
temp_probe = ds18b20_therm.DS18B20()

###### Wind #######

def reset_wind_observation():
    """reset wind reading"""
    global wind_count, wind_observation_start_time
    wind_count = 0
    wind_observation_start_time = time()

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

###### End Wind #######

###### Rainfall #######

def reset_rainfall():
    """reset rain reading"""
    global tip_count
    tip_count = 0

def tip():
    """record tip of rain bucket"""
    global tip_count
    tip_count += 1
    # print("Total rain (mm) " + str(rain_mm))

rain_sensor.when_pressed = tip

###### End Rainfall #######

while True:
    recording_start = time()
    while time() - recording_start <= recording_interval:

        reset_wind_observation()
        store_directions.append(wind_direction_byo.get_value(wind_interval))

        speed_this_interval = calculate_speed(time() - wind_observation_start_time)
        store_speeds.append(speed_this_interval)

    wind_speed = mean(store_speeds)
    wind_gust = max(store_speeds)
    wind_direction = wind_direction_byo.get_average(store_directions)

    rain_mm = tip_count * BUCKET_CAPACITY

    # humidity, pressure, ambient_temp = bme280_sensor.read_all()

    ground_temp = temp_probe.read_temp()

    print(wind_speed, wind_gust, wind_direction, rain_mm, ground_temp)

    store_speeds = []
    store_directions = []
    reset_rainfall()
