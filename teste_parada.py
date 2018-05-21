import logging
import time
import cflib.crtp
import trajetorias as tr
import threading
import paralelo
import combinacao

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.log import LogConfig

URI1 = 'radio://0/80/250K/E7E7E7E7E1'

cflib.crtp.init_drivers(enable_debug_driver=False)
factory = CachedCfFactory(rw_cache='./cache')

scf1 = SyncCrazyflie(URI1, cf=Crazyflie(rw_cache='./cache'))
scf1.open_link()
mc1 = MotionCommander(scf1)

def pouso_emergencial(mc):
    entrada = input("1 para cancelar: ")
    if(entrada == '1'):
        mc.setStopMotion(True)


threadEmergencial = threading.Thread(target=pouso_emergencial, args=(mc1, ))
threadEmergencial.setDaemon(True)
threadEmergencial.start()

pr = paralelo.Paralelo(mc1)
pr.putCommand(paralelo.TAKEOFF, mc1)
pr.execute()

pr.putCommand(paralelo.LINEAR, mc1)
pr.execute()

mc1.setStopMotion(True)

pr.putCommand(paralelo.LINEAR, mc1)
pr.execute()

pr.putCommand(paralelo.LAND, mc1)
pr.execute()


scf1.close_link()
