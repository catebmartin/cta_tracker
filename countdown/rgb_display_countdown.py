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
    def __init__(self, list_location, image_location, offset_text = False, color=(255, 255, 255)):
        Countdown.__init__(self, list_location, image_location)
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
        days_until, event_display = Countdown.current_line_getter(self)
        matrix = self.matrix_getter()
        canvas = matrix.CreateFrameCanvas()
        canvas.SetImage(self.image_thumbnail)
        #TODO: If event is too long, assert
        text_start = 0
        if self.offset_text:
            text_start += (self.image_thumbnail.width+2)
        available_screen = matrix.width-text_start
        print_lst = [str(days_until)+' days', 'until', event_display]
        start_lst = [text_start+((available_screen-(len(x)*4))/2) for x in print_lst]
        height_lst = [8, 18, 28]
        graphics.DrawText(canvas, self.font, start_lst[0], height_lst[0], self.color, print_lst[0])
        graphics.DrawText(canvas, self.font, start_lst[1], height_lst[1], self.color, print_lst[1])
        graphics.DrawText(canvas, self.font, start_lst[2], height_lst[2], self.color, print_lst[2])
        matrix.SwapOnVSync(canvas)
        time.sleep(3)
