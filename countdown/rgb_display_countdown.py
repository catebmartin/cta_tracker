from countdown.countdown import Countdown
from PIL import Image
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


class RGBDisplayCountdown(Countdown):
    # TODO: consider RGBDisplay master class. Inherit constructor, font loader, color loader
    def __init__(self, date_of_event, event_display, image_location):
        Countdown.__init__(self, date_of_event, event_display, image_location)
        self.font = RGBDisplayCountdown.font_loader(self)
        # self.color = make a color loader, dependent on user input

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
        font.LoadFont("/home/cat_pi0/rpi-rgb-led-matrix/fonts/5x7.bdf")  # TODO: relative path
        return font

    def display_countdown(self):
        matrix = self.matrix_constructor()
        self.canvas = matrix.CreateFrameCanvas()
        self.canvas.SetImage(self.image_thumbnail)
        #matrix.SetImage(self.image_thumbnail)
        graphics.DrawText(self.canvas, self.font, 16, 8, graphics.Color(255, 255, 255), str(self.date_of_event)+' days until')
        graphics.DrawText(self.canvas, self.font, 16, 24, graphics.Color(255, 255, 255), self.event_display)
        self.canvas = matrix.SwapOnVSync(self.canvas)
        time.sleep(15)