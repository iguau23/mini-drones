import logging
import time
from threading import Timer
import combinacao

import cflib.crtp  # noqa
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


URI1 = 'radio://0/80/2M/E7E7E7E7E3'


logging.basicConfig(level=logging.ERROR)


def stab_log_data( timestamp, data, logconf):
    """Callback froma the log API when data arrives"""
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

if __name__ == '__main__':
# Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    cf = Crazyflie(rw_cache='./cache')
    sync = SyncCrazyflie(URI1, cf=cf)
    sync.open_link()

    # Connect some callbacks from the Crazyflie API
    #cf.connected.add_callback(connected)

    time.sleep(2)
    lg_stab = LogConfig(name='Kalman Variance', period_in_ms=100)
    lg_stab.add_variable('kalman.varPX', 'float')
    lg_stab.add_variable('kalman.varPY', 'float')
    lg_stab.add_variable('kalman.varPZ', 'float')

    try:
        cf.log.add_config(lg_stab)
        #This callback will receive the data
        lg_stab.data_received_cb.add_callback(stab_log_data)
        # Start the logging
        lg_stab.start()
    except AttributeError:
        print('Could not add Stabilizer log config, bad configuration.')

    mc = MotionCommander(sync)
    combinacao.combinacao1(mc)
    sync.close_link()
