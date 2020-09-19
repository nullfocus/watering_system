DEBUG = True

clock = None
datastore = None
device = None

import logging, os
logging.basicConfig(
    level=logging.DEBUG, 
    filename='log.txt', 
    format='%(asctime)s %(message)s'
)

log = logging.getLogger(os.path.basename(__file__)).debug

log('starting...')

#wraps the system clock
from clock import Clock 
clock = Clock(log)
 
#data storage / retrieval layer
from datastore_sqlite import DatastoreSqlite
datastore = DatastoreSqlite(log)

#for debugging seperately from the raspberry pi
if DEBUG:
    from device_stub import DeviceStub
    device = DeviceStub(log)
else:
    from device_rpi import DeviceRpi
    device = DeviceRpi(log)    

#put it all together
from orchestrator import Orchestrator
orchestrator = Orchestrator(log, clock, device, datastore)

from interval_worker import IntervalWorker
worker = IntervalWorker(log, orchestrator.update, 15)
worker.start()

#start up the flask api
import api 
api.start(log, orchestrator)
