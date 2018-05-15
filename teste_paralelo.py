import logging
import time
import cflib.crtp
import trajetorias as tr
import threading
import paralelo

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

URI1 = 'radio://0/80/250K/E7E7E7E7E7'
URI2 = 'radio://0/80/250K/E7E7E7E7EA'

cflib.crtp.init_drivers(enable_debug_driver=False)
factory = CachedCfFactory(rw_cache='./cache')

scf1 = SyncCrazyflie(URI1, cf=Crazyflie(rw_cache='./cache'))
scf1.open_link()
mc1 = MotionCommander(scf1)
# scf2 = SyncCrazyflie(URI2, cf=Crazyflie(rw_cache='./cache'))
# scf2.open_link()
# mc2 = MotionCommander(scf2)
# mcs = {mc1, mc2}


pr = paralelo.Paralelo(mc1)
pr.putCommand(paralelo.TAKEOFF, mc1)
# pr.putCommand(paralelo.TAKEOFF, mc2)
pr.execute()

#pr.putCommand(paralelo.UP, mc1)
# pr.putCommand(paralelo.TAKEOFF, mc2)
pr.execute()

pr.putCommand(paralelo.HORARIO, mc1)
# pr.putCommand(paralelo.HORARIO, mc2)
pr.execute()

pr.putCommand(paralelo.ZIGUEZAGUE, mc1)
# pr.putCommand(paralelo.ZIGUEZAGUE, mc2)
pr.execute()

pr.putCommand(paralelo.DIAGONAL, mc1)
# pr.putCommand(paralelo.DIAGONAL, mc2)
pr.execute()

pr.putCommand(paralelo.ARCO, mc1)
# pr.putCommand(paralelo.DEGRAU, mc2)
pr.execute()

pr.putCommand(paralelo.LOOP, mc1)
pr.execute()

pr.putCommand(paralelo.ESPIRAL, mc1)
pr.execute()

pr.putCommand(paralelo.LAND, mc1)
# pr.putCommand(paralelo.LAND, mc2)
pr.execute()



scf1.close_link()
# scf2.close_link()
