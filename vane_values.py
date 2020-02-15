
POSITIONS = [
        {'deg': 0, 'r2': 33000},
        {'deg': 22.5, 'r2': 6570},
        {'deg': 45, 'r2': 8200},
        {'deg': 67.5, 'r2': 891},
        {'deg': 90, 'r2': 1000},
        {'deg': 112.5, 'r2': 688},
        {'deg': 135, 'r2': 2200},
        {'deg': 157.5, 'r2': 1410},
        {'deg': 180, 'r2': 3900},
        {'deg': 202.5, 'r2': 3140},
        {'deg': 225, 'r2': 16000},
        {'deg': 247.5, 'r2': 14120},
        {'deg': 270, 'r2': 120000},
        {'deg': 292.5, 'r2': 42120},
        {'deg': 315, 'r2': 64900},
        {'deg': 337.5, 'r2': 21880},
        ]

def voltage_divider(r1, r2, vin):
    vout = vin * (r2/(r1+r2))
    return round(vout,3)

def output_table(r1,vin):
    """
    For a given value of a set r2, find voltage out for variable r1
    """
    print('%-20s' % "Direction (Degrees)",
            '%-17s' % "Resistance (Ohms)",
            '%-12s' % "Vout Voltage")
    for position in POSITIONS:
        print('%-20.2f' % position['deg'],
                '%-17.2f' % position['r2'],
                '%-12.1f' % voltage_divider(r1,position['r2'], vin))

output_table(10000,5)
