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
from builtins import input

ARCO        = '1'
DEGRAU      = '2'
HORARIO     = '3'
LINEAR      = '4'
ZIGUEZAGUE  = '5'
DIAGONAL    = '6'
LOOP        = '7'
ESPIRAL     = '8'
QUIT        = 's'
TAKEOFF     = 'takeoff'
UP          = 'up'
DOWN        = 'down'
LAND        = 'land'
command     = 'start'
commandsList = [ARCO, DEGRAU, HORARIO, LINEAR, ZIGUEZAGUE, DIAGONAL,
                LOOP, ESPIRAL, TAKEOFF, LAND, UP, DOWN]
validCommmand = True

messageComando =("Escolha um comando:\n"
                 "(1) - arco\n"
                 "(2) - degrau\n"
                 "(3) - horario\n"
                 "(4) - linear\n"
                 "(5) - ziguezague\n"
                 "(6) - diagonal\n"
                 "(7) - loop\n"
                 "(8) - espiral\n"
                 "(s) - sair\n")

URI1 = 'radio://0/80/250K/E7E7E7E7E7'
URI2 = 'radio://0/80/250K/E7E7E7E7EA'
URI3 = 'radio://0/80/250K/E7E7E7E7E9'
uris = [URI1, URI2, URI3]


cflib.crtp.init_drivers(enable_debug_driver=False)
factory = CachedCfFactory(rw_cache='./cache')

message = 'Quais drones deseja controlar? (1, 2, 3 ou combinação delas): '
user_input = input(message)

selected = []
if(user_input.find('1')!=-1):
    selected.append(1)
if(user_input.find('2')!=-1):
    selected.append(2)
if(user_input.find('3')!=-1):
    selected.append(3)

scf = []
mcs = []
for i in selected:
    sync = SyncCrazyflie(uris[i-1], cf=Crazyflie(rw_cache='./cache'))
    sync.open_link()
    mcs.append(MotionCommander(sync))
    scf.append(sync)

selectedCommands = []
for j in selected:
    print("\npara o drone %d" %j)
    selectedCommands.append(input(messageComando))

pr = paralelo.Paralelo(mcs)

for mc in mcs:
    pr.putCommand(paralelo.TAKEOFF, mc)
pr.execute()

for k in selected:
    pr.putCommand(selectedCommands[k-1], mcs[k-1])

pr.execute()

for l in selected:
    pr.putCommand(paralelo.LAND, mcs[l-1])
pr.execute()

for sync in scf:
    sync.close_link()
