from kivymd.uix.screen import MDScreen

class StartPage(MDScreen):
    '''Start Page'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'start'
