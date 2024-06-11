from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from components.cards.rating_card import RatingCard

class RatingPage(MDScreen):
    '''Rating Page'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'rating'

    def on_kv_post(self, base_widget):
        self.fill_comands()

    def fill_comands(self):
        list_layout = MDList()
        for i in range(1, 21):
            item = RatingCard(number=f"{i}", team_name=f"Team", time=f"{i*1000}")
            list_layout.add_widget(item)
        self.scrollView.add_widget(list_layout)
