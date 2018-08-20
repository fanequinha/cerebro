from __future__ import print_function

import math
import time

from dronekit import LocationGlobalRelative, VehicleMode, connect

import settings


class Engine(object):

    def __init__(self, connection_string, baudrate):
        self.connection_string = connection_string
        self.baudrate = baudrate

        if settings.USE_SITL is True:
            import dronekit_sitl
            sitl = dronekit_sitl.start_default()
            self.connection_string = sitl.connection_string()

    def connect(self, wait_ready=True):
        self._vehicle = connect(self.connection_string,
                                baud=self.baudrate,
                                wait_ready=wait_ready)

    def set_mode(self, mode):
        self._vehicle.mode = VehicleMode(mode)

        while not self._vehicle.mode.name == mode:
            print(" Waiting for mode change to %s..." % mode)
            time.sleep(1)

    def arm(self):
        self._vehicle.armed = True
        while not self._vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

    def disarm(self):
        self._vehicle.armed = False
        while self._vehicle.armed:
            print(" Waiting for disarming...")
            time.sleep(1)

    @property
    def vehicle(self):
        return self._vehicle

    def goto(self, latitude, longitude):
        dest = LocationGlobalRelative(latitude, longitude, 0)
        self._vehicle.simple_goto(dest)
        return

    # location returns the current location of the ardusub
    def location(self):
        return self._vehicle.location.global_frame

    def wait_until_location(self, latitude, longitude):
        # @todo Wait until the reached location is in there
        return True


class Mision(Engine):

    final_lat = 0
    final_lon = 0
    earth_radio = 6378137

    def __init__(self, *args, **kwargs):
        super(Mision, self).__init__(*args, **kwargs)
        self.connect()
        self.set_start_point(
            kwargs.get("lat", 0),
            kwargs.get("lon", 0))

    def set_start_point(self, latitude, longitude):
        self.goto(latitude, longitude)
        self.wait_until_location(latitude, longitude)
        return

    def move_north(self, meters=10):
        location = self.location()
        new_lat = location.lat
        dLat = meters/self.earth_radio
        new_lat = location.lat + dLat * 180 / math.Pi
        return self.goto(new_lat, location.lon)

    def move_east(self, meters=10):
        location = self.location()
        new_lon = location.lon
        dLon = meters / (self.earth_radio * math.Cos(math.Pi * location.lat / 180))
        new_lon = location.lon + dLon * 180 / math.Pi
        return self.goto(location.lat, new_lon)

    def set_final_location(self, lat, lon):
        self.final_lat = lat
        self.final_lon = lon
