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

URI1 = 'radio://0/80/250K/E7E7E7E7E1'
URI2 = 'radio://0/80/250K/E7E7E7E7E2'

cflib.crtp.init_drivers(enable_debug_driver=False)
factory = CachedCfFactory(rw_cache='./cache')

scf1 = SyncCrazyflie(URI1, cf=Crazyflie(rw_cache='./cache'))
scf1.open_link()
mc1 = MotionCommander(scf1)
scf2 = SyncCrazyflie(URI2, cf=Crazyflie(rw_cache='./cache'))
scf2.open_link()
mc2 = MotionCommander(scf2)

combinacao.combinacao2(mc1, mc2)

scf1.close_link()
scf2.close_link()
