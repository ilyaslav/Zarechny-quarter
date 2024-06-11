from kivymd.uix.screen import MDScreen

class RuningGamePage(MDScreen):
    '''Runing Game Page'''
    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)
        self.name = 'runing_game'
