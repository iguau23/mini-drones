import logging
import time
import math
import trajetorias
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/250K/E7E7E7E7E2'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
cflib.crtp.init_drivers(enable_debug_driver=False)

with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
    #We take off when the commander is created
    # cf = scf.cf
    # cf.param.set_value('kalman.resetEstimation', '1')
    # time.sleep(0.1)
    # cf.param.set_value('kalman.resetEstimation', '0')
    # time.sleep(2)
    with MotionCommander(scf) as mc:
        time.sleep(2)
