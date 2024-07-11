import time
from typing import Union
import RPi.GPIO as GPIO


class ultrasonic:
    def __init__(self, trigger_pin: int, echo_pin: int, GPIO_Mode = None, min_range: float = 2E-2, max_range: float = 4) -> None:
        """
        Parameters:
        trigger_pin (int): pin that creates the ultrasonic pulse
        echo_pin (int): pin that receives the ultrasonic pulse back
        GPIO_Mode: The way the Raspberry Pi pinout is chosen to be laid out
        max_range (float): The maxiumum range of the ultrasonic sensor
        min_range (float): The miniumum range of the ultrasonic sensor
        """
        
        self.__trigger_pin: int = trigger_pin # pin that creates pulse
        self.__echo_pin: int = echo_pin # pin that recives pulse in
        self.max_range: float = max_range
        self.min_range: float = min_range

        # constants 
        self.SPEED_OF_SOUND: float = 343.21 # speed of sound in meters per second at 20 deg C
        self.PULSE_WIDTH: float = 10E-6 # pulse width in seconds

        # setup
        if GPIO_Mode:
            GPIO.setmode(GPIO_Mode)
        GPIO.setup(self.__trigger_pin, GPIO.OUT)
        GPIO.setup(self.__echo_pin, GPIO.IN)


    def send_pulse(self):
        """
        Sends pulse of predefined width out of the sensor
        """
        GPIO.output(self.__trigger_pin, True)
        time.sleep(self.PULSE_WIDTH)
        GPIO.output(self.__trigger_pin, False)

    def recv_pulse(self, falling_edge: bool = True , timeout: float = 0 ) -> Union[float, None]:
        """
        Recives pulse

        Parameters:
        falling_edge (bool): Sets if the time should be return on the rising or falling edge of the pulse
        timeout (float): Timeout before pulse signal deemed to be lost. Defaults to 1.05 the time it takes the signal to go the max distance and back 

        Returns:
        Union[float, None]: Seconds since monitoring started for pulse
                            If pulse is not found before timeout None is returned
        """
        if timeout <= 0:
            timeout = (self.max_range/self.SPEED_OF_SOUND)*1.05*2

        GPIO_falling_edge = GPIO.HIGH if (falling_edge) else GPIO.LOW 
        t_pulse_start = time.time() # not actual pulse start time just reusing var to determin if it's good to start measuring
        # wait for pulse condition to start
        while (GPIO.input(self.__echo_pin) != GPIO_falling_edge):
            if ((time.time() - t_pulse_start) >= timeout):
                return None
        
        # start as pulse can now be track for a falling or rising edge depending on how falling_edge var is set
        t_pulse_start = time.time()
        while (GPIO.input(self.__echo_pin) == GPIO_falling_edge):
            if ((time.time() - t_pulse_start) >= timeout):
                return None

        return time.time()-t_pulse_start

    def get_distance(self):
        """
        Gets distance in meters the object is from the ultrasonic sensor

        Returns:
        Union[float, None]: Meters the object is from the ultrasonic sensor
                            If unable to calculate distance None is returned
        """
        self.send_pulse()
        time_traveled = self.recv_pulse()
        if not time_traveled:
            return None
        meters = self.SPEED_OF_SOUND*time_traveled/2
        return max(min(meters, self.max_range), self.min_range)

    def __del__(self):
        GPIO.cleanup([self.__trigger_pin, self.__echo_pin])

if __name__ == "__main__":
    us = ultrasonic(trigger_pin=27, echo_pin=22, GPIO_Mode=GPIO.BCM)
    dist = us.get_distance()
    if dist:
        print(dist*100, "cm")
