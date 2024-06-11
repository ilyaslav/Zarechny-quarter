class Team:
    def __init__(self, team_name = '', status= 'не начата',
                 quest1= 0, quest2= 0, quest3= 0, quest4= 0,
                 start_time= None, game_time= None) -> None:
        self.team_name = team_name
        self.status = status
        self.quest = {
            'quest1':  quest1,
            'quest2':  quest2,
            'quest3':  quest3,
            'quest4':  quest4,
        }
        self.start_time = start_time
        self.game_time = game_time
