from countdown.countdown import Countdown
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class RGBDisplayCountdown(Countdown):
    # TODO: consider RGBDisplay master class. Inherit constructor, font loader, color loader
    # TODO: center and wrap text automatically
    def __init__(self, date_of_event, event_display, image_location, color=(255,255,255)):
        Countdown.__init__(self, date_of_event, event_display, image_location)
        self.font = RGBDisplayCountdown.font_loader(self)
        self.color = graphics.Color(color[0], color[1], color[2])

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
        font.LoadFont("fonts/4x6.bdf")
        return font

    def display_countdown(self):
        self.days_until = Countdown.set_days_until(self)
        matrix = self.matrix_constructor()
        self.canvas = matrix.CreateFrameCanvas()
        self.canvas.SetImage(self.image_thumbnail)
        #TODO: figure out how to center this
        graphics.DrawText(self.canvas, self.font, 22, 6, self.color, str(self.days_until)+' days')
        graphics.DrawText(self.canvas, self.font, 28, 16, self.color, 'until')
        graphics.DrawText(self.canvas, self.font, 18, 26, self.color, self.event_display)
        self.canvas = matrix.SwapOnVSync(self.canvas)
        time.sleep(3)