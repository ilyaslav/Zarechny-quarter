from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

class QuestCard(MDCard):
    text = StringProperty()
    function = ObjectProperty()
