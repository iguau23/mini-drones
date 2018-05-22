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

def combinacao1(mc):
    pr = paralelo.Paralelo(mc)

    pr.putCommand(paralelo.TAKEOFF, mc)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc)
    pr.execute()

    pr.putCommand(paralelo.ZIGUEZAGUE, mc)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.ARCO, mc)
    pr.execute()

    pr.putCommand(paralelo.LOOP, mc)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc)
    pr.execute()

    pr.putCommand(paralelo.ESPIRAL, mc)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc)
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
    mcs={mc1, mc2}
    pr = paralelo.Paralelo(mcs)

    pr.putCommand(paralelo.TAKEOFF, mc1)
    pr.putCommand(paralelo.TAKEOFF, mc2)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1, dist=0.5)
    pr.putCommand(paralelo.LINEAR, mc2, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.ZIGUEZAGUE, mc1, dist=0.5)
    pr.putCommand(paralelo.ZIGUEZAGUE, mc2, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc2, dist=0.7)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.ZIGUEZAGUE, mc1, dist=0.5)
    pr.putCommand(paralelo.ZIGUEZAGUE, mc2, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.LOOP, mc1, dist=0.6)
    pr.putCommand(paralelo.LOOP, mc2, dist=0.6)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc2, dist=0.7)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1, dist=0.5)
    pr.putCommand(paralelo.LINEAR, mc2, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.ESPIRAL, mc1, dist=0.5)
    pr.putCommand(paralelo.ESPIRAL, mc2, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc2, dist=0.7)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1, dist=0.5)
    pr.putCommand(paralelo.LINEAR, mc2, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.ZIGUEZAGUE, mc1, dist=0.5)
    pr.putCommand(paralelo.ZIGUEZAGUE, mc2, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc2, dist=0.7)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.LAND, mc1)
    pr.putCommand(paralelo.LAND, mc2)
    pr.execute()

def circulo(mc1, mc2):
    mcs={mc1, mc2}
    pr = paralelo.Paralelo(mcs)

    pr.putCommand(paralelo.TAKEOFF, mc1)
    pr.putCommand(paralelo.TAKEOFF, mc2)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1, dist=0.5)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.execute()

    pr.putCommand(paralelo.CIRCULO, mc1)
    pr.putCommand(paralelo.CIRCULO, mc2)
    pr.execute()

    pr.putCommand(paralelo.LINEAR, mc1)
    pr.putCommand(paralelo.LINEAR, mc2)
    pr.execute()

    pr.putCommand(paralelo.TURNRIGHT, mc1)
    pr.putCommand(paralelo.TURNRIGHT, mc2)
    pr.execute()

    pr.putCommand(paralelo.LAND, mc1)
    pr.putCommand(paralelo.LAND, mc2)
    pr.execute()


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
