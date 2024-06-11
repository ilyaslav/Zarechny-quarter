from Database import db
from Team import Team
from time import time

QUESTION1 = 'Задание 1'
QUESTION2 = 'Задание 2'
QUESTION3 = 'Задание 3'
QUESTION4 = 'Задание 4'

class Game:
    def __init__(self) -> None:
        self.team = Team()
        self.category = ''
        self.question = [
            QUESTION1,
            QUESTION2,
            QUESTION3,
            QUESTION4
        ]
        self.tasks = {
            QUESTION1: 'ответ 1',
            QUESTION2: 'ответ 2',
            QUESTION3: 'ответ 3',
            QUESTION4: 'ответ 4',
        }

    def get_time(self):
        return time() - self.team.start_time

    def reg_team(self, team_name):
        self.team = Team(team_name=team_name)
        db.add_team(self.category, team_name)

    def start_game(self):
        t = int(time())
        self.team = Team(
            team_name=self.team.team_name,
            status='начата',
            start_time=t
            )
        db.start_game(self.category, self.team.team_name, t)

    def team_exists(self, team_name):
        return db.team_exists(self.category, team_name)

    def choose_team(self, team_name):
        self.team = Team(*db.get_team(self.category, team_name))

    def compleate_quest(self, quest):
        quest_id = self.question.index(quest)+1
        self.team.quest[f'quest{quest_id}'] = 1
        db.set_quest(self.category,
                     self.team.team_name,
                     f'quest{quest_id}'
                    )

    def finish_game(self, team_name, time):
        db.finish_game(self.category, team_name, time)

    def check_game_status(self):
        return not 0 in self.team.quest.values()

    def get_quest(self, number):
        return self.team.quest[f'quest{number}']

    def check_answer(self, question, answer):
        return self.tasks[question] == answer.lower()
