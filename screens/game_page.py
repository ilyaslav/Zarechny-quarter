from kivymd.uix.screen import MDScreen

class GamePage(MDScreen):
    '''Game Page'''
    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)
        self.name = 'game'
