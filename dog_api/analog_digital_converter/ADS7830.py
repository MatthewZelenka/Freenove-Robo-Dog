from smbus2 import SMBus, i2c_msg

class ADS7830:
    def __init__(self, bus:int | str = 0, address:int = 0x48) -> None:
        # i2c bus for raspberry pi (1)
        self.bus = SMBus(bus)
        # i2c address for the device default set to 0x48
        self.address = address
    def post(self, SD: bool | int, channel_selector: int, power_mode: int) -> int:
        """
        Parameters:
        SD (bool | int): Single-Ended/Differential Inputs
                   0: Differential Inputs
                   1: Single-Ended Inputs
        channel_selector (int): Channel Selection 0 to 7
        power_mode: Power-Down Selection
                    0: Power Down Between A/D Converter Conversions
                    1: Internal Reference OFF and A/D Converter ON
                    2: Internal Reference ON and A/D Converter OFF
                    3: Internal Reference ON and A/D Converter ON
        """
        # input range check
        if SD < 0 or SD > 1:
            raise IndexError("SD index out of range: {}".format(SD))

        if channel_selector < 0 or channel_selector > 7:
            raise IndexError("channel_selector index out of range: {}".format(channel_selector))

        if power_mode < 0 or power_mode > 3:
            raise IndexError("power_mode index out of range: {}".format(power_mode))
        
        # creates command based of of byte required from spec sheet
        command = (SD << 7) | (channel_selector << 4) | (power_mode << 2)
        self.bus.write_byte(self.address, command)
        data = self.bus.read_byte(self.address)
        return data
    
if __name__ == "__main__":
    ADC = ADS7830(bus=1)
    print(ADC.post(SD=1, channel_selector=0, power_mode=1))
