import logging
import time
import cflib.crtp
import trajetorias as tr
import threading
import paralelo
import positionControl as pc

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from builtins import input


cflib.crtp.init_drivers(enable_debug_driver=False)
factory = CachedCfFactory(rw_cache='./cache')



position   = [1]
cornersList = [1,3,5,7]
validCommmand = True
user_input_numbers = 'start'
user_input_command = 'start'
messageComando =("Escolha um comando:\n"
                 "(1) - arco\n"
                 "(2) - degrau\n"
                 "(3) - linear\n"
                 "(4) - ziguezague\n"
                 "(5) - loop\n"
                 "(6) - espiral\n"
                 "(s) - sair\n")
message = 'Quais drones deseja controlar? (1, 2, 3 ou combinacao delas): '
URI1 = 'radio://0/80/250K/E7E7E7E7E7'
URI2 = 'radio://0/80/250K/E7E7E7E7EA'
URI3 = 'radio://0/80/250K/E7E7E7E7E9'
uris = [URI1, URI2, URI3]
while(user_input_command != 's'):

    user_input_numbers = input(message)

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
        position[j-1] = pc.newPosition(position[j-1])


    pr = paralelo.Paralelo(mcs)

    for mc in mcs:
        pr.putCommand(paralelo.TAKEOFF, mc)
    pr.execute()

    for k in selected:
        pr.putCommand(selectedCommands[k-1], mcs[k-1])
    pr.execute()

    for m in selected:
        if(position[m-1] in cornersList):
            pr.putCommand(paralelo.TURNRIGHT, mcs[l-1])
        pr.execute()


    for l in selected:
        pr.putCommand(paralelo.LAND, mcs[l-1])
    pr.execute()

    for sync in scf:
        sync.close_link()
