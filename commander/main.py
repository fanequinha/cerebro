#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import settings
from engine import Engine


def main():
    connection_string = settings.DEFAULT_SERIAL_PORT
    baud_rate = settings.DEFAULT_BAUD_RATE

    if arg_options.connect:
        connection_string = arg_options.connect
    if arg_options.baud_rate:
        baud_rate = arg_options.baud_rate

    engine = Engine(connection_string, baudrate=baud_rate)
    engine.connect()
    vehicle = engine.vehicle

    print(" Autopilot Firmware version: %s" % vehicle.version)
    print(" System status: %s" % vehicle.system_status.state)
    print(" Mode: %s" % vehicle.mode.name)
    print(" Armed: %s" % vehicle.armed)

    while arg_options.listen:
        print(vehicle.location.global_frame)
        print(vehicle.attitude)
        print(" Velocity: %s" % vehicle.velocity)
        print(vehicle.gps_0)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Command line program to interact with the Pixhawk')
    parser.add_argument(
        "-c", "--connect", help="""Vehicle connection string
        ('/dev/tty.SLAB_USBtoUART', '/dev/cu.usbmodem1', etc.).
        If not specified other parameters, SITL automatically started and used.""")
    parser.add_argument("-b", "--baud-rate", type=int,
                        help="Serial baud rate: 57600 | Usb connection: 115200")
    parser.add_argument("-l", "--listen", action='store_true',
                        help="Listen location, attitude, velocity and gps")

    return parser


if __name__ == "__main__":

    parser = get_parser()
    arg_options = parser.parse_args()

    main()
