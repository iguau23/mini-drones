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



dronePosition   = [1, 3, 5]
cornersList = [1,3,5,7]
validCommmand = True
user_input_numbers = 'start'
user_input_command = 'start'
messageComando =("(1) - arco\n"
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
    if(user_input_numbers.find('1')!=-1):
        selected.append(1)
    if(user_input_numbers.find('2')!=-1):
        selected.append(2)
    if(user_input_numbers.find('3')!=-1):
        selected.append(3)
    if(len(selected)==0):
        print("\n===============================================================================\n"
              "     Obrigado por terem utilizado o nosso mini-drones program!\n"
              "                      Espero que tenham gostado!\n"
              "===============================================================================\n")
        break

    scf = []
    mcs = []

    for i in selected:
        sync = SyncCrazyflie(uris[i-1], cf=Crazyflie(rw_cache='./cache'))
        sync.open_link()
        mcs.append(MotionCommander(sync))
        scf.append(sync)

    selectedCommands = []
    for i in selected:
        print("\nEscolha um comando para o drone %d, que está na posição %d" %(i, dronePosition[i-1]))
        selectedCommands.append(input(messageComando))
        dronePosition[i-1] = pc.newPosition(dronePosition[i-1])

    print("executando")
    pr = paralelo.Paralelo(mcs)

    for mc in mcs:
        pr.putCommand(paralelo.TAKEOFF, mc)
    #pr.execute()

    for i in range(len(selected)):
        pr.putCommand(selectedCommands[i-1], mcs[i-1])
    #pr.execute()

    for i in range(len(selected)):
        if(dronePosition[i-1] in cornersList):
            pr.putCommand(paralelo.TURNRIGHT, mcs[i-1])
        #pr.execute()


    for i in range(len(selected)):
        pr.putCommand(paralelo.LAND, mcs[i-1])
    #pr.execute()
    print("pronto\n")

    for sync in scf:
        sync.close_link()
