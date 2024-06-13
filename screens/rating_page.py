from kivymd.uix.screen import MDScreen

class RatingPage(MDScreen):
    '''Rating Page'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'rating'
