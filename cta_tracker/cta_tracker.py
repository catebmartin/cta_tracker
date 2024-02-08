import requests
import time

from cta_tracker.secrets import api_key

class CTAtracker():
    def __init__(self, url_args):
        self.url_args = url_args
        self.url = CTAtracker.url_constructor(self)
        self.json_response = CTAtracker.curl_api(self)
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

    def curl_api(self):
        """
        Requests url and returns specific portion of json.
        """
        r = requests.get(self.url)
        if 'eta' in r.json()['ctatt']:
            return r.json()['ctatt']['eta']
        else:
            #no trains. Sleep and return empty train list
            time.sleep(5)
            print('No train')
            return {}