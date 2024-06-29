from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty


class RatingCard(MDBoxLayout):
    team_name = StringProperty()
    time = StringProperty()
    number = StringProperty()
    halign = StringProperty()
