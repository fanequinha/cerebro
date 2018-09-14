#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import time

import settings
from boat import Boat

logging.basicConfig(
    format='%(levelname)s : %(module)s : %(asctime)s : %(message)s',
    filename='commander.log', level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main():
    connection_string = settings.DEFAULT_SERIAL_PORT
    baud_rate = settings.DEFAULT_BAUD_RATE

    if arg_options.connect:
        connection_string = arg_options.connect
    if arg_options.baud_rate:
        baud_rate = arg_options.baud_rate

    boat = Boat(connection_string, baudrate=baud_rate)
    boat.connect(wait_ready=False)
    vehicle = boat.vehicle

    while not vehicle.attitude.pitch:
        logger.debug(" Waiting for vehicle to initialise...")
        time.sleep(1)

    logger.debug("Autopilot Firmware version: %s", vehicle.version)
    logger.debug("Mode: %s", vehicle.mode.name)
    logger.debug("System status: %s", vehicle.system_status)
    logger.debug("Armed: %s", vehicle.armed)

    while arg_options.listen:
        listen_data = "Location: %s -  %s - Groundspeed: %s" % \
                      (boat.location, boat.vehicle.attitude,
                                         boat.vehicle.groundspeed)
        logger.debug(listen_data)
        time.sleep(2)

    if arg_options.goto:
        boat.arm()
        boat.set_mode('GUIDED')
        lat, lon = arg_options.goto.split(',')

        boat.goto(lat, lon)
        boat.vehicle.close()


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
                        help="Listen location, attitude and groundspeed")
    parser.add_argument("-g", "--goto",
                        help="Move to a GPS point (Decimal format). Ex. '42.227870, -8.7218401'")

    return parser


if __name__ == "__main__":

    parser = get_parser()
    arg_options = parser.parse_args()

    main()
