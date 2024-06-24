import sqlite3

def error_handler(func):
	def wrappper(*args, **kwargs):
		try:
			data = func(*args, **kwargs)
			return data
		except Exception as e:
			print(e)
			return -1
	return wrappper

class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('game.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    @error_handler
    def team_exists(self, table_name, team_name):
        with self.connection:
            sql = f"SELECT * FROM {table_name} WHERE team_name = ?"
            params = (team_name,)
            result = self.cursor.execute(sql, params).fetchmany(1)
            return bool(len(result))

    @error_handler
    def get_team(self, table_name, team_name):
        with self.connection:
            sql = "SELECT tn.team_name, st.status, tn.quest1, tn.quest2, tn.quest3,"+\
                 f" tn.quest4, tn.start_time, tn.game_time FROM {table_name} tn,"+\
                 " status_table st WHERE team_name = ? AND tn.status = st.id"
            params = (team_name,)
            result = self.cursor.execute(sql, params).fetchmany(1)[0]
            return result

    @error_handler
    def get_rating(self, table_name):
          with self.connection:
            sql = f"SELECT team_name, game_time FROM {table_name} WHERE status = 3 ORDER BY game_time"
            result = self.cursor.execute(sql).fetchall()
            return result[:100]

    @error_handler
    def add_team(self, table_name, team_name):
          with self.connection:
            sql = f"INSERT INTO {table_name} (team_name) VALUES (?)"
            params = (team_name,)
            self.cursor.execute(sql, params)
            self.connection.commit()

    @error_handler
    def start_game(self, table_name, team_name, start_time):
          with self.connection:
            print(start_time)
            sql = f"UPDATE {table_name} SET start_time = ?, status = 1 WHERE team_name = ?"
            params = (start_time, team_name)
            self.cursor.execute(sql, params)
            self.connection.commit()

    @error_handler
    def set_quest(self, table_name, team_name, quest):
          with self.connection:
            sql = f"UPDATE {table_name} SET {quest} = 1 WHERE team_name = ?"
            params = (team_name,)
            self.cursor.execute(sql, params)
            self.connection.commit()

    @error_handler
    def finish_game(self, table_name, team_name, time):
          with self.connection:
            sql = f"UPDATE {table_name} SET game_time = ?, status = 3 WHERE team_name = ?"
            params = (time, team_name)
            self.cursor.execute(sql, params)
            self.connection.commit()

    @error_handler
    def get_help(self, table_name, team_name, time):
         with self.connection:
            sql = f"UPDATE {table_name} SET start_time = ? WHERE team_name = ?"
            params = (time, team_name)
            self.cursor.execute(sql, params)
            self.connection.commit()

db = Database()
if __name__ == "__main__":
    print(db.set_quest('children_table', 'qwe', 'quest1'))
