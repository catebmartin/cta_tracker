import datetime
import sys
from cta_tracker.cta_tracker import CTAtracker

time_args={
    'peak_start':datetime.time(7,0,0),
    'peak_end':datetime.time(10,0,0),
    'sleep_start':datetime.time(22,0,0),
    'sleep_end':datetime.time(2,0,0),
}

url_args={
    'stpid':[],
    'mapid':['40570'],
    'max_results':8
}

cta = CTAtracker(time_args, url_args)

try:
    print('Keyboard interrupt supported.')
    cta.api_loop()
except KeyboardInterrupt:
    sys.exit(0)