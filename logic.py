import sqlite3
from config import DATABASE
from random import randint

class DB_Manager:
    
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE favorite (
                         id INTEGER PRIMARY KEY,
                         user_id TEXT,
                         title TEXT
                          
                        )''') 

            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
            
    def get_title_movie(self,title):
        return self.__select_data(sql = 'SELECT title FROM movies WHERE title = ?', data = (title,))
    
    def get_genre_movie(self,title):
        return self.__select_data(sql = 'SELECT genre FROM movies WHERE title = ?', data = (title,))

    def get_overview_movie(self,title):
        return self.__select_data(sql = 'SELECT overview FROM movies WHERE title = ?', data = (title,))
    
    def get_random_movie(self):
        return self.__select_data(sql = 'SELECT * FROM movies ORDER BY RANDOM() LIMIT 1')[0]
    
    def add_favorite(self,user,title):
        return self.__select_data(sql = 'INSERT INTO favorite (user_id,title) VALUES (?,?)', data = (user,title))
    
    def delete_favorite(self,title):
        return self.__select_data(sql = 'DELETE FROM favorite WHERE title = ?', data = (title,))
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.delete_favorite('HARRY POTTER')
