#!/usr/bin/env python3
"""
rollsmart.py is the main entry point script to interact with the rollsmart

TO DO: Basically everything
"""
import fire
from rich import print
from rich.traceback import install; install()

import bno055
import max30105

class Rollsmart:
    def __init__(self):
        """
        Currently only initialized the CLI text art :)
        """
        self.initialize_cli()
        self.connect_sensors()

    def connect_sensors(self):
        """
        Establishes connection with all of the sensors on RollSmart upon waking
        """
        self.IMU = bno055()
        self.HR = max30105()


    def initialize_cli(self):
        """
        Prints CLI welcome message
        """
        print("[deep_sky_blue1 bold]                    _       _                                      _      ")
        print("[deep_sky_blue1 bold]     _ _    ___     | |     | |     ___    _ __    __ _      _ _   | |_   ")
        print("[deep_sky_blue1 bold]    | '_|  / _ \    | |     | |    (_-<   | '  \  / _` |    | '_|  |  _|  ")
        print("[deep_sky_blue1 bold]   _|_|_   \___/   _|_|_   _|_|_   /__/_  |_|_|_| \__,_|   _|_|_   _\__|  ")
        print('[dark_violet] _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| ')
        print("[dark_violet] "'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-')




if __name__ == '__main__':
    fire.Fire(Rollsmart())
