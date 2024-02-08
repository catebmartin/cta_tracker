from datetime import datetime
import time

from countdown.rgb_display_countdown import RGBDisplayCountdown
from cta_tracker.rgb_display_cta import RGBDisplayCTA


class LEDDisplay:
    def __init__(self, time_args, url_args):
        self.time_setter(time_args)
        self.url_setter(url_args)

    def time_setter(self, time_args):
        """
        Check that input time args are acceptable.  If they pass, set values.
        :param time_args: Dictionary of datetime fields
        :return: None. set time related init values
        """
        assert set(time_args.keys()) == {'peak_end', 'peak_start', 'sleep_end', 'sleep_start'}, 'Incorrect time keys'
        assert ~self.time_in_range(time_args['peak_start'], time_args['peak_end'],
                                   time_args['sleep_start']), 'Sleep start overlap with peak'
        assert ~self.time_in_range(time_args['peak_start'], time_args['peak_end'],
                                   time_args['sleep_end']), 'Sleep end overlap with peak'
        assert ~self.time_in_range(time_args['sleep_start'], time_args['sleep_end'],
                                   time_args['peak_start']), 'Peak start overlap with sleep'
        assert ~self.time_in_range(time_args['sleep_start'], time_args['sleep_end'],
                                   time_args['peak_end']), 'Peak end overlap with sleep'
        self.peak_start = time_args['peak_start']
        self.peak_end = time_args['peak_end']
        self.sleep_start = time_args['sleep_start']
        self.sleep_end = time_args['sleep_end']

    def url_setter(self, url_args):
        """
        Check that input url_args are acceptable.
        :param url_args: Dictionary of various fields
        :return: None. init url_args
        """
        # confirm that there are no extra key values
        assert set(url_args.keys()).issubset({'stpid', 'mapid', 'max_results'}), 'Incorrect url args'
        # for key values that are input, confirm that they are of the correct type
        type_dct = {
            'stpid': list,
            'mapid': list,
            'max_results': int
        }
        for key, value in type_dct.items():
            if key in url_args.keys():
                assert isinstance(url_args[key], value), f'Incorrect value for {key}'
        self.url_args = url_args

    @staticmethod
    def time_in_range(start, end, test_time=datetime.now().time()):
        """
        Return true if current time is in the range [start, end].
        input:
            start:datetime.time()
            end:datetime.time()
        output:
            boolean
        """
        # TODO add unit tests
        if start <= end:
            return start <= test_time <= end
        else:
            return start <= test_time or test_time <= end

    def loop_display(self):
        # image handling is slow, so do it once up front
        milo_countdown = RGBDisplayCountdown('2024-06-24', 'Milo\'s BDay', 'images/milo_sticker.jpg', (204, 102, 0))
        f1_countdown = RGBDisplayCountdown('2024-02-29', 'Bahrain', 'images/ferrari.jpg')
        while True:
            is_peak = self.time_in_range(self.peak_start, self.peak_end)
            is_sleep = self.time_in_range(self.sleep_start, self.sleep_end)
            if is_peak:
                rgb_display = RGBDisplayCTA(self.url_args)
                rgb_display.display_json_response()
            elif is_sleep:
                # do nothing. Sleep 10 minutes
                time.sleep(10 * 60)
            else:
                # display countdowns
                milo_countdown.display_countdown()
                f1_countdown.display_countdown()
                # display CTA tracker
                rgb_display = RGBDisplayCTA(self.url_args)
                rgb_display.display_json_response()
