import datetime
import sys
from led_display import LEDdisplay

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


led_display = LEDdisplay(time_args, url_args)

try:
    print('Keyboard interrupt supported.')
    led_display.loop_display()
except KeyboardInterrupt:
    sys.exit(0)