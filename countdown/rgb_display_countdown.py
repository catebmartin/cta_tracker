from countdown.countdown import Countdown
from PIL import Image
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


class RGBDisplayCountdown(Countdown):
    # TODO: consider RGBDisplay master class. Inherit constructor, font loader, color loader
    # TODO: center and wrap text automatically
    def __init__(self, date_of_event, event_display, image_location):
        Countdown.__init__(self, date_of_event, event_display, image_location)
        self.font = RGBDisplayCountdown.font_loader(self)
        self.days_until = Countdown.set_days_until(self)
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
        font.LoadFont("/home/cat_pi0/rpi-rgb-led-matrix/fonts/4x6.bdf")  # TODO: relative path
        return font

    def display_countdown(self):
        matrix = self.matrix_constructor()
        self.canvas = matrix.CreateFrameCanvas()
        self.canvas.SetImage(self.image_thumbnail)
        #TODO: figure out how to center this
        color = graphics.Color(204,102,0)
        graphics.DrawText(self.canvas, self.font, 22, 6, color, str(self.days_until)+' days')
        graphics.DrawText(self.canvas, self.font, 28, 16, color, 'until')
        graphics.DrawText(self.canvas, self.font, 18, 26, color, self.event_display)
        self.canvas = matrix.SwapOnVSync(self.canvas)
        time.sleep(3)