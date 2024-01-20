from datetime import datetime
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from cta_tracker.cta_tracker import CTAtracker
class RGBDisplayCTA(CTAtracker):
    def __init__(self, url_args):
        CTAtracker.__init__(self, url_args)
        self.font = RGBDisplayCTA.font_loader(self)
        """
        Class that will take JSON return by CTA API and display it in RGB. 
        """
    def matrix_constructor(self):
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        options.drop_privileges = False
        return RGBMatrix(options=options)
    def font_loader(self):
        font = graphics.Font()
        font.LoadFont("/home/cat_pi0/rpi-rgb-led-matrix/fonts/5x7.bdf")
        return font

    @staticmethod
    def get_color(dest_in):
        if dest_in == "O'Hare":
            return graphics.Color(255, 255, 255) #white
        if dest_in in ["Forest Park", "UIC-Halsted"]:
            return graphics.Color(0,157,255) #ctablue
        return graphics.Color(255,255,255)
    def scroll_one_train(self, train1):
        '''
        Take in details of two trains.  Led will scroll details 3 times before ending.
        :param train1: Json with details of train1
        :param train2: Json with details of train2
        :return: None. Display will be on LED Matrix
        '''
        matrix = self.matrix_constructor()
        self.canvas = matrix.CreateFrameCanvas()

        station1 = train1['destNm']
        difference1 = (datetime.strptime(train1['arrT'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(train1['prdt'],
                                                                                                '%Y-%m-%dT%H:%M:%S'))
        time_until1 = str(int(divmod(difference1.total_seconds(), 60)[0]))
        scroll_cutoff_idx = 13 #the led column at which left scroll stops for stations
        iter_count, scroll_count = 0, 0
        textColor1 = RGBDisplayCTA.get_color(station1)
        while scroll_count <= 3:
            self.canvas.Clear()
            graphics.DrawText(self.canvas, self.font, 1, 8, graphics.Color(255, 255, 255), time_until1)
            # start placement at left near cutoff.  Loop through and remove letters off the front
            graphics.DrawText(self.canvas, self.font, scroll_cutoff_idx, 8, textColor1, station1[iter_count:])
            self.canvas = matrix.SwapOnVSync(self.canvas)
            if iter_count == 0:
                #extra long sleep at start, so text pauses a bit
                time.sleep(2)
            time.sleep(0.25)
            iter_count += 1
            if iter_count > len(station1):
                #restart scroll
                iter_count = 0
                scroll_count+=1
    def scroll_two_trains(self, train1, train2):
        # TODO: create functions for a lot of this, now that it's reused in scroll_one_train
        '''
        Take in details of two trains.  Led will scroll details 3 times before ending.
        :param train1: Json with details of train1
        :param train2: Json with details of train2
        :return: None. Display will be on LED Matrix
        '''
        matrix = self.matrix_constructor()
        self.canvas = matrix.CreateFrameCanvas()

        station1 = train1['destNm']
        station2 = train2['destNm']
        difference1 = (datetime.strptime(train1['arrT'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(train1['prdt'],
                                                                                                '%Y-%m-%dT%H:%M:%S'))
        time_until1 = str(int(divmod(difference1.total_seconds(), 60)[0]))
        difference2 = (datetime.strptime(train2['arrT'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(train2['prdt'],
                                                                                                '%Y-%m-%dT%H:%M:%S'))
        time_until2 = str(int(divmod(difference2.total_seconds(), 60)[0]))

        scroll_cutoff_idx = 13 #the led column at which left scroll stops for stations
        iter_count, scroll_count = 0, 0
        textColor1 = RGBDisplayCTA.get_color(station1)
        textColor2 = RGBDisplayCTA.get_color(station2)
        while scroll_count <= 3:
            self.canvas.Clear()
            graphics.DrawText(self.canvas, self.font, 1, 8, graphics.Color(255, 255, 255), time_until1)
            graphics.DrawText(self.canvas, self.font, 1, 24, graphics.Color(255, 255, 255), time_until2)
            # start placement at left near cutoff.  Loop through and remove letters off the front
            graphics.DrawText(self.canvas, self.font, scroll_cutoff_idx, 8, textColor1, station1[iter_count:])
            graphics.DrawText(self.canvas, self.font, scroll_cutoff_idx, 24, textColor2, station2[iter_count:])
            self.canvas = matrix.SwapOnVSync(self.canvas)
            if iter_count == 0:
                # extra long sleep at start, so text pauses a bit
                time.sleep(2)
            time.sleep(0.25)
            iter_count += 1
            if iter_count > max(len(station1), len(station2)):
                # restart scroll
                iter_count = 0
                scroll_count+=1
    def display_json_response(self):
        # TODO: Add unit tests. There have been issues in the past.
        # look at self.json response. how many trains in it?
        train_pair_count = round(len(self.json_response)/2)
        for i in range(0,train_pair_count*2,2):
            if i+1 < len(self.json_response):
                # train2 exists
                train1 = self.json_response[i]
                train2 = self.json_response[i+1]
                self.scroll_two_trains(train1, train2)
            else:
                train1 = self.json_response[i]
                self.scroll_one_train(train1)