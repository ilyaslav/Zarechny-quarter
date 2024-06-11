from kivymd.uix.screen import MDScreen

class QuestPage(MDScreen):
    '''Quest Page'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'quest'
