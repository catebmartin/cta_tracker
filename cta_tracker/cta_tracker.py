import requests
import time
import datetime
import pytz

from cta_tracker.secrets import api_key


class CTATracker:
    def __init__(self, url_args):
        self.url_args = url_args
        self.url = CTATracker.url_constructor(self)
        self.json_response = CTATracker.curl_api(self)
        """
        Class that will ping CTA API and return relevant information in JSON format. 
        """
    def url_constructor(self):
        """
        supported kwargs:
            stpid: list of strings representing different stop-directions
            mapid: list of strings representing different stops
            max_results: integer representing number of trains to return
        """
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

    def curl_api(self):
        """
        Requests url and returns specific portion of json.
        At times connection is weak and request is denied.
        """
        try:
            # we receive a return from the request
            r = requests.get(self.url)
            if 'eta' not in r.json()['ctatt']:
                # we receive a return but no trains. Sleep and return empty train list
                time.sleep(5)
                print(f'No train at {datetime.datetime.now(pytz.timezone("America/Chicago"))}')
                return {}
            return r.json()['ctatt']['eta']
        except Exception as e:
            # the request was not successful.  Store error and sleep.
            print(f'Exception {e} at {datetime.datetime.now(pytz.timezone("America/Chicago"))}')
            return {}
