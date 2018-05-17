import logging
import time
from threading import Timer

import cflib.crtp  # noqa
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig


URI1 = 'radio://0/80/250K/E7E7E7E7E3'


logging.basicConfig(level=logging.ERROR)


def connected(self):
    self._lg_stab = LogConfig(name='Battery', period_in_ms=100)
    self._lg_stab.add_variable('pm.vbat', 'float')

    try:
        self._cf.log.add_config(self._lg_stab)
        # This callback will receive the data
        self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
        # Start the logging
        self._lg_stab.start()
    except AttributeError:
        print('Could not add Stabilizer log config, bad configuration.')

    t = Timer(5, self._cf.close_link)
    t.start()

def stab_log_data( timestamp, data, logconf):
    """Callback froma the log API when data arrives"""
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

if __name__ == '__main__':
# Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    cf = Crazyflie(rw_cache='./cache')

    # Connect some callbacks from the Crazyflie API
    #cf.connected.add_callback(connected)



    print('Connecting to %s' % URI1)
    # Try to connect to the Crazyflie
    scf = cf.open_link(URI1)
    print('Connected to %s' % URI1)

    time.sleep(2)
    lg_stab = LogConfig(name='Battery', period_in_ms=100)
    lg_stab.add_variable('pm.vbat', 'float')

    #try:
    cf.log.add_config(lg_stab)
    # This callback will receive the data
    lg_stab.data_received_cb.add_callback(stab_log_data)
    # Start the logging
    lg_stab.start()
    #except AttributeError:
        #print('Could not add Stabilizer log config, bad configuration.')
    time.sleep(5)
    cf.close_link()
