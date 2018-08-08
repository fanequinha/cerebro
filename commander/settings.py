import os

DEVELOPMENT = False

# Add your custom serial port
# (http://python.dronekit.io/guide/connecting_vehicle.html#get-started-connecting)
DEFAULT_SERIAL_PORT = os.environ['SERIAL_PORT']
# Add port baud rate. Tipically 57600 for serial, 115200 for USB.
# Check PixHawk TELEM 1 configuration in case connection problems.
DEFAULT_BAUD_RATE = os.environ['BAUD_RATE']
