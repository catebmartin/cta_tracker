class RGBDisplay():
    def __init__(self, json_response):
        self.json_response = json_response
        """
        Class that will take JSON return by CTA API and display it in RGB. 
        """

#sample code that works in ad hoc basis
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.roww = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
matrix = RGBMatrix(options = options)

offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("/home/cat_pi0/rpi-rgb-led-matrix/fonts/5x5.bdf") #store path elsewhere

min1 = '2'
loc1 = 'California'
min2 = '14'
loc2 = ('Logan Square')
scroll_cutoff = 13
iter_count = 0
if loc1 == loc2:
    textColor1 = graphics.Color(255,255,255) #white
    textColor2 = graphics.Color(255,255,255) #white
else:
    textColor1 = graphics.Color(255,255,255) #white
    textColor2 = graphics.Color(0,157,255) #cta blue
while True:
    offscreen_canvas.Clear()
    graphics.DrawText(offscreen_canvas, font, 1, 8, textColor1, min1)
    graphics.DrawText(offscreen_canvas, font, 1, 24, textColor1, min2)
    #start placement at left near cutoff.  Loop through and remove letters off the front
    graphics.DrawText(offscreen_canvas, font, scroll_cutoff, textColor1, loc1[:iter_count])
    graphics.DrawText(offscreen_canvas, font, scroll_cutoff, textColor2, loc2[:iter_count])
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    if iter_count == 0:
        time.sleep(2)
    time.sleep(0.25)
    iter_count+=1
    if iter_count > max(len(loc1), len(loc2)):
        iter_count = 0