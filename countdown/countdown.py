from datetime import date
from PIL import Image


class Countdown:
    """
    image_location: String to path of txt file containing relevent information
    image_location: String of path to display image location
    """

    def __init__(self,
                 list_location,
                 image_location):
        self.list_location = list_location
        self.image_location = image_location
        self.image_thumbnail = Countdown.image_getter(self)

    @staticmethod
    def get_line_date(current_line):
        current_line_date = current_line.split(',')[0]
        date_elements = current_line_date.split('-')
        date_elements = [int(x) for x in date_elements]
        return date(date_elements[0], date_elements[1], date_elements[2])

    def current_line_getter(self):
        d_today = date.today()
        d_line, n_line = date(2024, 1, 1), 'No event'  # dummy date to start loop with

        f = open(self.list_location)
        while d_line < d_today:
            current_line = f.readline()
            d_line = self.get_line_date(current_line)
            n_line = current_line.split(',')[1]
        return (d_line - d_today).days, n_line

    def image_getter(self):
        """Load and convert image"""
        image = Image.open(self.image_location)
        image.thumbnail((64, 32), Image.ANTIALIAS)
        return image.convert('RGB')

