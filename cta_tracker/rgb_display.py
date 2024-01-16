from datetime import datetime
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
class RGBDisplay():
    def __init__(self, json_response_in):
        self.json_response = json_response_in
        self.maxtrix = RGBDisplay.matrix_constructor(self)
        self.font = RGBDisplay.font_loader(self)
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
        return RGBMatrix(options=options)
    def font_loader(self):
        font = graphics.Font()
        font.LoadFont("/home/cat_pi0/rpi-rgb-led-matrix/fonts/5x5.bdf")
        return font

    def scroll_two_trains(self, train1, train2):
        '''
        Take in details of two trains.  Led will scroll details 3 times before ending.
        :param train1: Json with details of train1
        :param train2: Json with details of train2
        :return: None. Display will be on LED Matrix
        '''
        station1 = train1['staNm']
        station2 = train2['staNm']
        self.canvas = self.matrix.CreateFrameCanvas()
        difference1 = (datetime.strptime(train1['arrT'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(train['prdt'],
                                                                                                '%Y-%m-%dT%H:%M:%S'))
        time_until1 = str(divmod(difference1.total_seconds(), 60)[0])
        difference2 = (datetime.strptime(train2['arrT'], '%Y-%m-%dT%H:%M:%S') - datetime.strptime(train['prdt'],
                                                                                                '%Y-%m-%dT%H:%M:%S'))
        time_until2 = str(divmod(difference2.total_seconds(), 60)[0])
        scroll_cutoff_idx = 13 #the led column at which left scroll stops for stations
        iter_count, scroll_count = 0, 0
        if station1 == station2:
            textColor1 = graphics.Color(255, 255, 255)  # white
            textColor2 = graphics.Color(255, 255, 255)  # white
        else:
            textColor1 = graphics.Color(255, 255, 255)  # white
            textColor2 = graphics.Color(0, 157, 255)  # cta blue
        while scroll_count <= 3:
            self.canvas.Clear()
            graphics.DrawText(self.canvas, self.font, 1, 8, textColor1, time_until1)
            graphics.DrawText(self.canvas, self.font, 1, 24, textColor1, time_until2)
            # start placement at left near cutoff.  Loop through and remove letters off the front
            graphics.DrawText(self.canvas, self.font, scroll_cutoff_idx, textColor1, station1[:iter_count])
            graphics.DrawText(self.canvas, self.font, scroll_cutoff_idx, textColor2, station2[:iter_count])
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            if iter_count == 0:
                #extra long sleep at start, so text pauses a bit
                time.sleep(2)
            time.sleep(0.25)
            iter_count += 1
            if iter_count > max(len(station1), len(station2)):
                #restart scroll
                iter_count = 0
                scroll_count+=1
    def display_json_response(self):
        #look at self.json response. how many trains in it?
        train_pair_count = round(len(self.json_response.keys())/2)
        for i in range(0,train_pair_count+2,2):
            train1 = self.json_response[i]
            train2 = self.json_response[i+1]
            self.scroll_two_trains(train1, train2)

#sample code that works in ad hoc basis

# options = RGBMatrixOptions()
# options.row = 32
# options.cols = 64
# options.chain_length = 1
# options.parallel = 1
# options.hardware_mapping = 'adafruit-hat'
# matrix = RGBMatrix(options = options)
#
# offscreen_canvas = matrix.CreateFrameCanvas()
# font = graphics.Font()
# font.LoadFont("/home/cat_pi0/rpi-rgb-led-matrix/fonts/5x5.bdf") #store path elsewhere
#
# min1 = '2'
# loc1 = 'California'
# min2 = '14'
# loc2 = ('Logan Square')
# scroll_cutoff = 13
# iter_count = 0
# if loc1 == loc2:
#     textColor1 = graphics.Color(255,255,255) #white
#     textColor2 = graphics.Color(255,255,255) #white
# else:
#     textColor1 = graphics.Color(255,255,255) #white
#     textColor2 = graphics.Color(0,157,255) #cta blue
# while True:
#     offscreen_canvas.Clear()
#     graphics.DrawText(offscreen_canvas, font, 1, 8, textColor1, min1)
#     graphics.DrawText(offscreen_canvas, font, 1, 24, textColor1, min2)
#     #start placement at left near cutoff.  Loop through and remove letters off the front
#     graphics.DrawText(offscreen_canvas, font, scroll_cutoff, textColor1, loc1[:iter_count])
#     graphics.DrawText(offscreen_canvas, font, scroll_cutoff, textColor2, loc2[:iter_count])
#     offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
#     if iter_count == 0:
#         time.sleep(2)
#     time.sleep(0.25)
#     iter_count+=1
#     if iter_count > max(len(loc1), len(loc2)):
#         iter_count = 0