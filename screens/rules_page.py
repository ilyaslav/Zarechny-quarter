from kivymd.uix.screen import MDScreen

class RulesPage(MDScreen):
    '''Rules Page'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'rules'
