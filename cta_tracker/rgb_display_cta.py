from datetime import datetime
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from cta_tracker.cta_tracker import CTATracker


class RGBDisplayCTA(CTATracker):
    def __init__(self, url_args):
        CTATracker.__init__(self, url_args)
        self.font = self.font_getter()
        self.scroll_cutoff_idx = 13  # the LED column at which left scroll stops for stations
        """
        Class that will take JSON return by CTA API and display it in RGB. 
        """

    @staticmethod
    def matrix_getter():
        """
        Hard code settings for matrix.
            rows: number of rows in your LED display
            cols: number of cols in your LED display
            chain_lengths: number of displays chained together
            parallel: I believe this is the number of vertical displays but documentation is sparse
            hardware_mapping: Corresponds to the type of display
            drop_privileges: When running as sudo (recommended) this setting ensures that sudo persists
        :return: Matrix with options set
        """
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        options.drop_privileges = False
        return RGBMatrix(options=options)

    @staticmethod
    def font_getter():
        font = graphics.Font()
        font.LoadFont("fonts/5x7.bdf")
        return font

    @staticmethod
    def get_color(dest_in):
        if dest_in == "O'Hare":
            return graphics.Color(255, 255, 255)  # white
        if dest_in in ["Forest Park", "UIC-Halsted"]:
            return graphics.Color(0, 157, 255)  # cta blue
        return graphics.Color(255, 255, 255)

    @staticmethod
    def train_cleaner(train):
        difference = (datetime.strptime(train['arrT'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(train['prdt'], '%Y-%m-%dT%H:%M:%S'))
        arrival_time = datetime.strptime(train['arrT'], '%Y-%m-%dT%H:%M:%S').strftime('%I:%M %p')
        return {
            'station': train['destNm'],
            'time_until': str(int(divmod(difference.total_seconds(), 60)[0])),
            'text_color': RGBDisplayCTA.get_color(train['destNm']),
            'arrival_time': arrival_time,
            'scroll_text': f"{train['destNm']}  {arrival_time}"
        }

    @staticmethod
    def scroll_comparison(train1, train2):
        """
        If the text is not the same length, then spread it out to be.
        :param train1: Dictionary from train_cleaner
        :param train2: Dictionary from train_cleaner
        :return: Two dictionaries, train 1 and train2. Corrected 'scroll_text' if necessary.
        """
        assert len(train1['arrival_time']) == len(train2['arrival_time'])
        if len(train1['scroll_text']) != len(train2['scroll_text']):
            desired_len = max(len(train1['scroll_text']), len(train2['scroll_text']))
            mid_pad = desired_len - min(len(train1['station']), len(train2['station'])) - len(train1['arrival_time'])
            train1['scroll_text'] = train1['station'].ljust(mid_pad, ' ') + train1['arrival_time']
            train2['scroll_text'] = train2['station'].ljust(mid_pad, ' ') + train2['arrival_time']
            print(train1['scroll_text'])
            print(train2['scroll_text'])
            return train1, train2


    def scroll_one_train(self, train1):
        """
        Take in details of two trains.  Led will scroll details 3 times before ending.
        :param train1: Json with details of train1
        :return: None. Display will be on LED Matrix
        """
        matrix = self.matrix_getter()
        canvas = matrix.CreateFrameCanvas()

        train1 = self.train_cleaner(train1)
        iter_count, scroll_count = 0, 0

        while scroll_count < 2:
            canvas.Clear()
            # set time on top left
            graphics.DrawText(canvas, self.font, 1, 8, graphics.Color(255, 255, 255), train1['time_until'])
            # start destination name placement at left near cutoff.  Loop through and remove letters off the front
            graphics.DrawText(canvas, self.font, self.scroll_cutoff_idx, 8, train1['text_color'], train1['scroll_text'][iter_count:])
            canvas = matrix.SwapOnVSync(canvas)
            if iter_count == 0:
                # extra long sleep at start, so text pauses a bit
                time.sleep(2)
            time.sleep(0.25)
            iter_count += 1
            if iter_count > len(train1['station']):
                # restart scroll
                time.sleep(1)
                iter_count = 0
                scroll_count += 1

    def scroll_two_trains(self, train1, train2):
        # TODO: create functions for a lot of this, now that it's reused in scroll_one_train
        """
        Take in details of two trains.  Led will scroll details 3 times before ending.
        :param train1: Json with details of train1
        :param train2: Json with details of train2
        :return: None. Display will be on LED Matrix
        """
        matrix = self.matrix_getter()
        canvas = matrix.CreateFrameCanvas()

        train1 = self.train_cleaner(train1)
        train2 = self.train_cleaner(train2)
        train1, train2 = self.scroll_comparison(train1, train2)
        iter_count, scroll_count = 0, 0

        while scroll_count < 2:
            canvas.Clear()
            graphics.DrawText(canvas, self.font, 1, 8, graphics.Color(255, 255, 255), train1['time_until'])
            graphics.DrawText(canvas, self.font, 1, 24, graphics.Color(255, 255, 255), train2['time_until'])
            # start placement at left near cutoff.  Loop through and remove letters off the front
            graphics.DrawText(canvas, self.font, self.scroll_cutoff_idx, 8, train1['text_color'], train1['scroll_text'][iter_count:])
            graphics.DrawText(canvas, self.font, self.scroll_cutoff_idx, 24, train2['text_color'], train2['scroll_text'][iter_count:])
            matrix.SwapOnVSync(canvas)
            if iter_count == 0:
                # extra long sleep at start, so text pauses a bit
                time.sleep(2)
            time.sleep(0.25)
            iter_count += 1
            if iter_count > max(len(train1['station']), len(train2['station'])):
                # restart scroll
                time.sleep(1)
                iter_count = 0
                scroll_count += 1

    def display_json_response(self):
        # TODO: Add unit tests. There have been issues in the past.
        # look at self.json response. how many trains in it?
        train_pair_count = round(len(self.json_response)/2)
        for i in range(0, train_pair_count*2, 2):
            if i+1 < len(self.json_response):
                # train2 exists
                train1 = self.json_response[i]
                train2 = self.json_response[i+1]
                self.scroll_two_trains(train1, train2)
            else:
                train1 = self.json_response[i]
                self.scroll_one_train(train1)
