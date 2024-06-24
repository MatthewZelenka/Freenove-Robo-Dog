import math

class speed_of_sound():
    def __init__(self) -> None:
        """
        Gets speed of sound of an ideal gas in meters per second (m/s)

        """
        self._molar_gas_constant: float = 0
        self._adiabatic_index: float = 0
        self._temperature:float = 0
        self._molar_mass:float = 1
        self._speed_of_sound:float = 0
    
    @property
    def molar_gas_constant(self) -> float:
        """
        Molar gas constant in J*mol^-1*K^-1
        """
        return self._molar_gas_constant
    
    @molar_gas_constant.setter
    def molar_gas_constant(self, molar_gas_constant):
        if molar_gas_constant < 0:
            raise ValueError("Molar gas constant only accepts positive values.")
        self._molar_gas_constant = float(molar_gas_constant)
        self.__calc_speed_of_sound()

    @property
    def adiabatic_index(self) -> float:
        """
        Adiabatic index
        """
        return self._adiabatic_index
    
    @adiabatic_index.setter
    def adiabatic_index(self, adiabatic_index):
        if adiabatic_index < 0:
            raise ValueError("Molar gas constant only accepts positive values.")
        self._adiabatic_index = float(adiabatic_index)
        self.__calc_speed_of_sound()

    @property
    def temperature(self) -> float:
        """
        Temperature in kelvin (K)
        """
        return self._temperature
    
    @temperature.setter
    def temperature(self, temperature):
        if temperature < 0:
            raise ValueError("temperature is in kelvin. Only accepts positive values.")
        self._temperature = float(temperature)
        self.__calc_speed_of_sound()

    @property
    def molar_mass(self) -> float:
        """
        Molar mass in kg/mol
        """
        return self._molar_mass
    
    @molar_mass.setter
    def molar_mass(self, molar_mass):
        if molar_mass <= 0:
            raise ValueError("temperature is in kelvin. Only accepts positive values greater then zero.")
        self._molar_mass = float(molar_mass)
        self.__calc_speed_of_sound()

    def get_speed(self) -> float:
        """
        Speed of sound in meters per second (m/s)
        """
        return self._speed_of_sound

    def __calc_speed_of_sound(self):
        """
        Calculates speed of sound in meters per second (m/s)
        """
        self._speed_of_sound = math.sqrt((self.adiabatic_index * self.molar_gas_constant * self.temperature) / (self.molar_mass)) 


if __name__ == "__main__":
    SOS = speed_of_sound()

    SOS.molar_gas_constant = 8.3145
    SOS.adiabatic_index = 1.4
    SOS.temperature = 20 + 273.15
    SOS.molar_mass = 0.0289645

    print(SOS.get_speed())

