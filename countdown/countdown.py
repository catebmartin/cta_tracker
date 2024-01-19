from datetime import date

class Countdown():
    '''
    date_of_event: String of format 'yyyy-mm-dd'
    '''

    def __init__(self,
                 date_of_event,
                 event_display,
                 image_location):
        self.date_of_event = date_of_event
        self.event_display = event_display
        self.image_location = image_location
        self.days_until = Countdown.set_days_until(self)
        self.image_thumbnail = Countdown.load_convert_image(self)

    def set_days_until(self):
        date_elements = self.date_of_event.split('-')
        date_elements = [int(x) for x in date_elements]
        d0 = date(date_elements[0], date_elements[1], date_elements[2])
        d1 = date.today()
        days_until = (d0 - d1).days
        print(f'{days_until} days until {self.event_display}!')
        return days_until

    def load_convert_image(self):
        from PIL import Image
        image = Image.open(self.image_location)
        image.thumbnail(64, 32), Image.ANTIALIAS)
        return image.convert('RGB')