from countdown.countdown import Countdown
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


class RGBDisplayCountdown(Countdown):
    """
    Extension of Countdown class used to display the information.
    Instantiate once with parameters of Countdown (image load takes a long time).
    Place .display_countdown() in loop as desired.
    """
    # TODO: consider RGBDisplay master class. Inherit constructor, font loader, color loader
    # TODO: center and wrap text automatically
    def __init__(self, date_of_event, event_display, image_location, offset_text = False, color=(255, 255, 255)):
        Countdown.__init__(self, date_of_event, event_display, image_location)
        self.font = self.font_getter()
        self.offset_text = offset_text
        self.color = graphics.Color(color[0], color[1], color[2])

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
        font.LoadFont("fonts/4x6.bdf")
        return font

    def display_countdown(self):
        days_until = Countdown.days_until_getter(self)
        matrix = self.matrix_getter()
        canvas = matrix.CreateFrameCanvas()
        canvas.SetImage(self.image_thumbnail)
        #TODO don't hardcode height. split cols by 3
        if self.offset_text:
            image_end = self.image_thumbnail.width
            text_start = image_end+2
        else:
            text_start = 0
        available_screen = matrix.cols()-text_start
        print_lst = [str(days_until)+' days',
                     'until',
                     self.event_display]
        start_lst = [(available_screen-(len(x)*4))/2 for x in print_lst]
        graphics.DrawText(canvas, self.font, start_lst[0], 6, self.color, print_lst[0])
        graphics.DrawText(canvas, self.font, start_lst[1], 16, self.color, print_lst[1])
        graphics.DrawText(canvas, self.font, start_lst[2], 26, self.color, print_lst[2])
        #TODO: If event is too long, assert
        matrix.SwapOnVSync(canvas)
        time.sleep(3)
