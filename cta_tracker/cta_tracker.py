import os
import requests
from datetime import datetime
import time

from cta_tracker.rgb_display import RGBDisplay
from cta_tracker.secrets import api_key

class CTAtracker():
    def __init__(self, time_args, url_args):
        self.peak_start = time_args['peak_start']
        self.peak_end = time_args['peak_end']
        self.sleep_start = time_args['sleep_start']
        self.sleep_end = time_args['sleep_end']
        self.url_args = url_args
        self.url = CTAtracker.url_constructor(self)
        """
        Class that will ping CTA API and return relevant information in JSON format. 
        """
    def url_constructor(self):
        """
        supported kwargs:
            stpid: list of strings representing different stop-directions
            mapid: list of strings representing different stops
        """
        # TODO: check kwargs. Make sure there is nothing unsupported in there.
        url = f'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={api_key}&outputType=JSON'
        if 'stpid' in self.url_args.keys():
            for stop in self.url_args["stpid"]:
                url += f'&stpid={stop}'
        if 'mapid' in self.url_args.keys():
            for stop in self.url_args["mapid"]:
                url += f'&mapid={stop}'
        if 'max_results' in self.url_args.keys():
            url += f'&max={self.url_args["max_results"]}'
        return url

    @staticmethod
    def time_in_range(start, end):
        """
        Return true if current time is in the range [start, end].
        input:
            start:datetime.time()
            end:datetime.time()
        output:
            boolean
        """
        now = datetime.now().time()
        if start <= end:
            return start <= now <= end
        else:
            return start <= now or now <= end

    @staticmethod
    def curl_api(url_in):
        """
        Requests url and returns specific portion of json.
        """
        r = requests.get(url_in)
        return r.json()['ctatt']['eta']

    @staticmethod
    def json_cleaner(json_in):
        """
        Takes input json and parses desired information.
        Currently is a simple print statement, but future state will include RGB formatting.
        """
        for train in json_in:
            print(f"Station Name: {train['staNm']}")
            print(f"Direction: {train['stpDe']}")
            difference = (datetime.strptime(train['arrT'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(train['prdt'],
                                                                                                    '%Y-%m-%dT%H:%M:%S'))
            time_until = divmod(difference.total_seconds(), 60)[0]
            print(f"Time Until: {int(time_until)} min")
            if train['isDly'] == '1':
                print('IS DELAYED')
            print('\n\n')

    def api_loop(self):
        # TO DO: what if start /end times don't exist
        while True:
            isPeak = self.time_in_range(self.peak_start, self.peak_end)
            isSleep = self.time_in_range(self.sleep_start, self.sleep_end)
            if isPeak:
                # ping every 5 seconds
                json = self.curl_api(self.url)
                # self.json_cleaner(json)
                rgb_display = RGBDisplay(json)
                rgb_display.display_json_response()
                time.sleep(25)
            elif isSleep:
                # do nothing. Sleep 10 minutes
                time.sleep(10 * 60)
            else:
                # ping every minute
                json = self.curl_api(self.url)
                print(type(json))
                print(json)
                print("Type of json)")
                # self.json_cleaner(json)
                rgb_display = RGBDisplay(json)
                rgb_display.display_json_response()
                time.sleep(60)
            # os.system('cls')
            # print('REFRESH!')
            # os.system('cls')
