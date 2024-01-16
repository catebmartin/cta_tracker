import datetime
from cta_tracker.cta_tracker import CTAtracker

time_args={
    'peak_start':datetime.time(7,0,0),
    'peak_end':datetime.time(10,0,0),
    'sleep_start':datetime.time(22,0,0),
    'sleep_end':datetime.time(2,0,0),
}

url_args={
    'stpid':[],
    'mapid':['40570', '40571'],
    'max_results':8
}

cta = CTAtracker(time_args, url_args)
print(cta.peak_start)
print(cta.url)

cta.api_loop()