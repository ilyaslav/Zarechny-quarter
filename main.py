from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList

from screens.start_page import StartPage
from screens.game_page import GamePage
from screens.runing_game_page import RuningGamePage
from components.forms.login_form import LoginForm
from components.forms.registration_form import RegistrationForm
from components.forms.send_form import SendForm
from components.forms.help_form import HelpForm
from components.cards.rating_card import RatingCard

from Game import Game

LabelBase.register(name='PT Serif', fn_regular='fonts/PT_Serif-Web-Bold.ttf')
LabelBase.register(name='Helvetica', fn_regular='fonts/helvetica_bold.otf')

class QuestApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login = False
        self.time = 0
        self.timer = None
        self.game = Game()

    def build(self):
        Window.size = [1000, 600]
        #Window.maximize()
        #Window.fullscreen = True
        self.load_all_kv_files()
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.font_styles.update({
            "H1": ["Helvetica", 96, False, 0.15],
            "H2": ["Helvetica", 60, False, -0.05],
            "H3": ["Helvetica", 48, False, 0],
            "H4": ["Helvetica", 34, False, 0.25],
            "H5": ["Helvetica", 24, False, 0],
            "H6": ["Helvetica", 20, False, 0.15],
            "Subtitle1": ["Helvetica", 16, False, 0.15],
            "Subtitle2": ["Helvetica", 14, False, 0.1],
            "Body1": ["Helvetica", 16, False, 0.5],
            "Body2": ["Helvetica", 14, False, 0.25],
            "Button": ["Helvetica", 14, True, 1.25],
            "Caption": ["Helvetica", 12, False, 0.4],
            "Overline": ["Helvetica", 10, True, 1.5],
        })

        self.sm = ScreenManager()
        self.sm.add_widget(StartPage(name='start'))
        self.sm.add_widget(RuningGamePage(name='runing_game'))
        self.sm.add_widget(GamePage(name='game'))
        self.dialog = MDDialog()

        return self.sm

    def load_all_kv_files(self) -> None:
        Builder.load_file('screens/start_page.kv')
        Builder.load_file('screens/game_page.kv')
        Builder.load_file('screens/runing_game_page.kv')
        Builder.load_file('screens/rules_page.kv')
        Builder.load_file('screens/quest_page.kv')
        Builder.load_file('screens/rating_page.kv')
        Builder.load_file('components/cards/card.kv')
        Builder.load_file('components/cards/quest_card.kv')
        Builder.load_file('components/cards/rating_card.kv')
        Builder.load_file('components/forms/login_form.kv')
        Builder.load_file('components/forms/registration_form.kv')
        Builder.load_file('components/forms/send_form.kv')
        Builder.load_file('components/forms/help_form.kv')

    def show_login_dialog(self):
        self.close_dialog()
        self.dialog = MDDialog(
                type="custom",
                content_cls=LoginForm(),
            )
        self.dialog.open()

    def show_registration_dialog(self):
        self.close_dialog()
        self.dialog = MDDialog(
                type="custom",
                content_cls=RegistrationForm(),
            )
        self.dialog.open()

    def show_send_form(self, question):
        self.close_dialog()
        self.dialog = MDDialog(
                type="custom",
                content_cls=SendForm(question=question),
            )
        self.dialog.open()

    def show_help_form(self, text):
        self.close_dialog()
        self.dialog = MDDialog(
                type="custom",
                content_cls=HelpForm(help=text),
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def open_start_page(self):
        self.close_dialog()
        self.sm.transition = SlideTransition(direction='right')
        self.sm.current = 'start'

    def open_game_page(self):
        self.close_dialog()
        self.sm.transition = SlideTransition(direction='left')
        self.sm.current = 'game'

    def open_quest_page(self):
        self.close_dialog()
        self.configure_questCards()
        self.sm.transition = SlideTransition(direction='left')
        self.sm.current = 'runing_game'

    def reset_error(self):
        self.dialog.content_cls.textField.error = False
        self.dialog.content_cls.textField.helper_text = ''

    def set_error(self, error_text):
        self.dialog.content_cls.textField.text = ''
        self.dialog.content_cls.textField.error = True
        self.dialog.content_cls.textField.helper_text = error_text

    def start_timer(self):
        self.time = self.game.get_time()
        self.timer = Clock.schedule_interval(self.set_time, 1)

    def set_time(self, dt):
        self.time+= 1
        screen = self.sm.get_screen('runing_game')
        screen.quest.timer.text = self.get_time(self.time)
        screen.rating.selected_team.time = self.get_time(self.time)

    def set_children(self):
        self.game.category = 'children_table'
        self.show_login_dialog()
    def set_adults(self):
        self.game.category = 'adults_table'
        self.show_login_dialog()
    def set_families(self):
        self.game.category = 'families_table'
        self.show_login_dialog()

    def login_team(self):
        team_name = self.dialog.content_cls.textField.text
        if self.game.team_exists(team_name):
            self.game.choose_team(team_name)
            if self.game.team.status == "не начата":
                self.open_game_page()
                screen = self.sm.get_screen('game')
                self.set_selected_team(team_name, screen)
                self.get_rating(screen)
            elif self.game.team.status == "начата":
                self.open_quest_page()
                self.start_timer()
                screen = self.sm.get_screen('runing_game')
                self.set_selected_team(team_name, screen)
                self.get_rating(screen)
            else:
                self.open_quest_page()
                screen = self.sm.get_screen('runing_game')
                self.set_selected_team(team_name, screen)
                self.get_rating(screen)
        else:
            self.set_error('Неверное имя команды')

    def reg_team(self):
        team_name = self.dialog.content_cls.textField.text
        if not self.game.team_exists(team_name):
            self.game.reg_team(team_name)
            self.open_game_page()
            screen = self.sm.get_screen('game')
            self.set_selected_team(team_name, screen)
            self.get_rating(screen)
        else:
            self.set_error('Такая команда уже существует')

    def start_game(self):
        self.game.start_game()
        self.start_timer()
        self.open_quest_page()
        screen = self.sm.get_screen('runing_game')
        self.set_selected_team(self.game.team.team_name, screen)
        self.get_rating(screen)

    def exit(self):
        self.game = Game()
        self.time = 0
        if self.timer:
            self.timer.cancel()
        self.open_start_page()

    def configure_questCards(self):
        screen = self.sm.get_screen('runing_game')
        screen.quest.questCard1.text = self.game.question[0]
        screen.quest.questCard2.text = self.game.question[1]
        screen.quest.questCard3.text = self.game.question[2]
        screen.quest.questCard4.text = self.game.question[3]

        if self.game.get_quest(1):
            screen.quest.questCard1.text = 'Верный ответ'
            screen.quest.questCard1.button.opacity = 0
        else:
            screen.quest.questCard1.button.opacity = 1

        if self.game.get_quest(2):
            screen.quest.questCard2.text = 'Верный ответ'
            screen.quest.questCard2.button.opacity = 0
        else:
            screen.quest.questCard2.button.opacity = 1

        if self.game.get_quest(3):
            screen.quest.questCard3.text = 'Верный ответ'
            screen.quest.questCard3.button.opacity = 0
        else:
            screen.quest.questCard3.button.opacity = 1

        if self.game.get_quest(4):
            screen.quest.questCard4.text = 'Верный ответ'
            screen.quest.questCard4.button.opacity = 0
        else:
            screen.quest.questCard4.button.opacity = 1

    def check_answer(self, question, answer):
        if self.game.check_answer(question, answer):
            self.game.compleate_quest(question)
            self.configure_questCards()
            self.close_dialog()
            self.stop_game()
        else:
            self.set_error('Неверный ответ')

    def stop_game(self):
        if self.game.check_game_status():
            self.game.finish_game()
            if self.timer:
                self.timer.cancel()
            screen = self.sm.get_screen('runing_game')
            self.get_rating(screen)

    def set_selected_team(self, team_name, screen):
        if self.game.team.status == 'не начата':
            screen.rating.selected_team.opacity = 0
            screen.rating.selected_team.height = 0
        else:
            screen.rating.selected_team.opacity = 1
            screen.rating.selected_team.number = self.game.get_position()
            screen.rating.selected_team.team_name = team_name
            time = self.get_time(self.game.get_time())
            screen.rating.selected_team.time = time
            screen.quest.timer.text = time

    def get_rating(self, screen):
        list_layout = MDList()
        comands = self.game.get_rating()
        j = 0
        for i in comands:
            j+=1
            item = RatingCard(
                              number=f'{j}',
                              team_name=i[0],
                              time=self.get_time(i[1])
                              )
            list_layout.add_widget(item)
        screen.rating.scrollView.clear_widgets()
        screen.rating.scrollView.add_widget(list_layout)

    def get_help(self):
        if not self.game.team.status == 'окончена':
            print(self.game.team.status)
            self.time+=900
            text = self.game.get_help()
            self.show_help_form(text)

    def get_time(self, time):
        hours = int(time/3600)
        minutes = int(time/60 % 60)
        seconds = int(time%60)
        if hours < 10:
            hours = f'0{hours}'
        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        return f'{hours} : {minutes} : {seconds}'

if __name__ == "__main__":
    QuestApp().run()
