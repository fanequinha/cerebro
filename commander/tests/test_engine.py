import time

from engine import Engine


def test_connection(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    assert engine.vehicle is not None

    engine.vehicle.close()

def test_wait_armable_vehicle(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    while not engine.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    assert engine.vehicle.is_armable

    engine.vehicle.close()

def test_vehicle_mode(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    engine.set_mode('GUIDED')

    assert engine.vehicle.mode.name=='GUIDED'

    engine.vehicle.close()

def test_vehicle_armed(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    engine.arm()

    assert engine.vehicle.armed

    engine.vehicle.close()

def test_vehicle_armed_and_disarmed(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    engine.arm()
    assert engine.vehicle.armed

    engine.disarm()
    assert not engine.vehicle.armed

    engine.vehicle.close()

# def test_set_sail():
#     engine = Engine()

#     engine.connect(True)
#     print(engine.vehicle.location.global_frame.lat)
#     print(engine.vehicle.location.global_frame.lon)
#     engine.goto(-4.6540196, 55.3995094)

#     while engine.vehicle.location.global_frame.lat < -4:
#         print('Lat:', engine.vehicle.location.global_frame.lat)

#     assert engine.vehicle.location.global_frame.lat == -4.6540196
#     assert engine.vehicle.location.global_frame.lon == 55.3995094

#     engine.vehicle.close()