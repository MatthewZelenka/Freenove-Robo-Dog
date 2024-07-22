import numpy as np

from .ADS7830 import ADS7830

class battery():
    def __init__(self, bus: int = 0, ref_voltage: float = 2.5, state_of_charge_table : list[list[float]] | None = None) -> None:
        self.ADC = ADS7830(bus=bus)
        self.ref_voltage = ref_voltage

        self.state_of_charge_table = state_of_charge_table if state_of_charge_table != None else [
            [3, 3.2, 3.25, 3.3, 3.35, 3.4, 3.45, 3.5, 3.55, 3.6, 3.65, 3.7, 3.75, 3.8, 3.85, 3.9, 3.95, 4, 4.05, 4.1, 4.15, 4.2], # battery voltage
            [0, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100], # % of battery charge
        ]

    def voltage(self, channel: int = 0):
        return (self.ADC.post(SD=1, channel_selector=channel, power_mode=1)/255)*self.ref_voltage
    
    def SoC(self, channel: int):
        return np.interp(self.voltage(channel), self.state_of_charge_table[0], self.state_of_charge_table[1])

if __name__ == "__main__":
    batt = battery(bus=1, ref_voltage=5)

    while True: 
        print("Voltage: {}\nSoC: {}".format(batt.voltage(0), batt.SoC(0)))
