from gpiozero import MCP3008
from time import sleep, time
import math

TOLERANCE = 0.03 # volts

adc = MCP3008(channel=0)

# The mapping between voltage and cardinal direction.
# Commented values are the voltages specified for the direction by the spec.
# I've tuned the actual values for my specific vane.
vout_mapping = {
    "3.84" : 0,
    "2.0" : 22.5, # 1.98
    "2.26" : 45, # 2.25
    "0.42" : 67.5, # 0.41
    "0.46" : 90, # 0.45
    "0.32" : 112.5,
    "0.91" : 135, # 0.90
    "0.62" : 157.5,
    "1.41" : 180, # 1.40
    "1.2" : 202.5, # 1.19
    "3.09" : 225, # 3.08
    "2.93" : 247.5,
    "4.62" : 270,
    "4.04" : 292.5,
    "4.33" : 315,
    "3.44" : 337.5, # 3.43
}

def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

def get_value(period=5):
    values = []

    print("Measuring wind direction for %d seconds..." % period)
    start_time = time()

    while time() - start_time <= period:
        wind = round(adc.value * 5,2)
        for i, (vout, direction) in enumerate(vout_mapping.items()):
            if wind == 0:
                # Don't try to take a reading if the value is 0
                break
            elif abs(float(vout) - wind) <= TOLERANCE:
                values.append(direction)
                break
            # Uncomment this to help with calibration
            # elif i == len(vout_mapping.items()) - 1:
            #     print("Unknown Value", wind)
    return get_average(values)

while True:
    print(get_value(3))
