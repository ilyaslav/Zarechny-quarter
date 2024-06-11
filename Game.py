from Database import db
from Team import Team
from time import time

class Game:
    def __init__(self) -> None:
        self.team = Team()
        self.category = ''

    def reg_team(self, team_name):
        self.team = Team(team_name=team_name)
        db.add_team(self.category, team_name)

    def start_game(self, team_name):
        t = time()
        self.team = Team(
            team_name=team_name,
            status='начата',
            start_time=t
            )
        db.start_game(self.category, team_name, t)

    def team_exists(self, team_name):
        return db.team_exists(self.category, team_name)

    def choose_team(self, team_name):
        self.team = Team(db.get_team(self.category, team_name))

    def compleate_quest(self, team_name, quest):
        self.team.quest[quest] = 1
        db.set_quest(self.category, team_name, quest)

    def finish_game(self, team_name, time):
        db.finish_game(self.category, team_name, time)

    def check_game_status(self):
        return not 0 in self.team.quest.values()
