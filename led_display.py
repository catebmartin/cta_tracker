from datetime import datetime
import time

from countdown.rgb_display_countdown import RGBDisplayCountdown
from cta_tracker.rgb_display_cta import RGBDisplayCTA
from cta_tracker.cta_tracker import CTAtracker

class LEDdisplay():
    def __init__(self, time_args, url_args):
        self.peak_start = time_args['peak_start']
        self.peak_end = time_args['peak_end']
        self.sleep_start = time_args['sleep_start']
        self.sleep_end = time_args['sleep_end']
        self.url_args = url_args

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

    def loop_display(self):
        # TO DO: what if start /end times don't exist
        while True:
            isPeak = self.time_in_range(self.peak_start, self.peak_end)
            isSleep = self.time_in_range(self.sleep_start, self.sleep_end)
            if isPeak:
                rgb_display = RGBDisplayCTA(self.url_args)
                rgb_display.display_json_response()
            elif isSleep:
                # do nothing. Sleep 10 minutes
                time.sleep(10 * 60)
            else:
                milo_countdown = RGBDisplayCountdown('2024-06-24', 'Milo\'s Birthday', 'images/milo_sticker.jpg')
                milo_countdown.display_countdown()

                rgb_display = RGBDisplayCTA(self.url_args)
                rgb_display.display_json_response()