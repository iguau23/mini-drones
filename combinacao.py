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

def combinacao1(mc, dist = 0.8):
    pr = paralelo.Paralelo(mc)

    pr.putCommand(paralelo.TAKEOFF, mc)
    pr.execute()

    if(dist==0.5):
        pr.putCommand(paralelo.UP, mc)
        pr.execute()

    pr.putCommand(paralelo.LINEAR, mc, dist = dist)
    pr.execute()

    pr.putCommand(paralelo.ZIGUEZAGUE, mc, dist = dist)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc, dist = dist)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc, dist = dist)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc, dist=dist)
    pr.execute()

    pr.putCommand(paralelo.LOOP, mc, dist = dist)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc, dist = dist)
    pr.execute()

    pr.putCommand(paralelo.ESPIRAL, mc, dist = dist)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.LAND, mc)
    pr.execute()


def combinacao2(mc1, mc2):
    mcs={mc1, mc2}
    pr = paralelo.Paralelo(mcs)

    pr.putCommand(paralelo.TAKEOFF, mc1)
    pr.putCommand(paralelo.TAKEOFF, mc2)
    pr.execute()

    pr.putCommand(paralelo.ZIGUEZAGUE, mc1)
    pr.putCommand(paralelo.ZIGUEZAGUE, mc2)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1)
    pr.putCommand(paralelo.LINEAR, mc2)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.LOOP, mc1)
    pr.putCommand(paralelo.LOOP, mc2)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc1)
    pr.putCommand(paralelo.ARCO, mc2)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1)
    pr.putCommand(paralelo.LINEAR, mc2)
    pr.execute()

    pr.putCommand(paralelo.ESPIRAL, mc1)
    pr.putCommand(paralelo.ESPIRAL, mc2)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.LAND, mc1)
    pr.putCommand(paralelo.LAND, mc2)
    pr.execute()

def combinacao3(mc1, mc2, mc3):
    mcs={mc1, mc2, mc3}
    pr = paralelo.Paralelo(mcs)

    pr.putCommand(paralelo.TAKEOFF, mc1)
    pr.putCommand(paralelo.TAKEOFF, mc2)
    pr.putCommand(paralelo.TAKEOFF, mc3)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1)
    pr.putCommand(paralelo.LINEAR, mc2)
    pr.putCommand(paralelo.LINEAR, mc3)
    pr.execute()

    pr.putCommand(paralelo.ZIGUEZAGUE, mc1)
    pr.putCommand(paralelo.ZIGUEZAGUE, mc2)
    pr.putCommand(paralelo.ZIGUEZAGUE, mc3)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.putCommand(paralelo.TURNRIGHT, mc3)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc1)
    pr.putCommand(paralelo.ARCO, mc2)
    pr.putCommand(paralelo.ARCO, mc3)
    pr.execute()

    pr.putCommand(paralelo.LOOP, mc1)
    pr.putCommand(paralelo.LOOP, mc2)
    pr.putCommand(paralelo.LOOP, mc3)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.putCommand(paralelo.TURNRIGHT, mc3)
    pr.execute()

    pr.putCommand(paralelo.ESPIRAL, mc1)
    pr.putCommand(paralelo.ESPIRAL, mc2)
    pr.putCommand(paralelo.ESPIRAL, mc3)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1)
    pr.putCommand(paralelo.LINEAR, mc2)
    pr.putCommand(paralelo.LINEAR, mc3)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.putCommand(paralelo.TURNRIGHT, mc3)
    pr.execute()

    pr.putCommand(paralelo.LAND, mc1)
    pr.putCommand(paralelo.LAND, mc2)
    pr.putCommand(paralelo.LAND, mc3)
    pr.execute()

def esquadrilha(mc1, mc2):
    thread1 = threading.Thread(target=combinacao1, args=(mc1, 0.5))
    thread1.setDaemon(True)

    thread2 = threading.Thread(target=combinacao1, args=(mc2,))
    thread2.setDaemon(True)

    thread1.start()
    time.sleep(7)
    thread2.start()

    thread1.join()
    thread2.join()

def circulo(mc1, mc2):
    mcs={mc1, mc2}
    pr = paralelo.Paralelo(mcs)

    pr.putCommand(paralelo.TAKEOFF, mc1)
    pr.putCommand(paralelo.TAKEOFF, mc2)
    pr.execute()

    time.sleep(1)
    mc1.move_distance(2, 2, 0, velocity=0.8)
    time.sleep(1)
    mc1.turn_right(180)

    pr.putCommand(paralelo.CIRCULO, mc1)
    pr.putCommand(paralelo.CIRCULO, mc2)
    pr.execute()

    thread1 = threading.Thread(target=ajusteCirculo1, args=(mc1,))
    thread1.setDaemon(True)

    thread2 = threading.Thread(target=ajusteCirculo2, args=(mc2,))
    thread2.setDaemon(True)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

def ajusteCirculo1(mc):
    mc.turn_left(180)
    mc.forward(1, velocity=0.8)
    mc.turn_left(90)
    mc.forward(2, velocity = 0.8)
    mc.turn_left(90)
    mc.land()

def ajusteCirculo2(mc):
    mc.forward(1, velocity = 0.5)
    mc.turn_left(180)
    mc.land()

def combinacaoArcos(mc):
    pr = paralelo.Paralelo(mc)

    pr.putCommand(paralelo.TAKEOFF, mc)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.LAND, mc)
    pr.execute()
