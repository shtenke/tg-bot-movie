import config
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from logic import DB_Manager
from random import randint
from config import DATABASE
import sqlite3 
import json
manager = DB_Manager(DATABASE)
bot = telebot.TeleBot(config.API_TOKEN)

def self_info(bot, message, row):
        global user
        info = f"""
📍Title of movie:   {row[2]}
📍Year:                   {row[3]}
📍Genres:              {row[4]}
📍Rating IMDB:      {row[5]}


🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻
{row[6]}
"""
        user = message.chat.id
        bot.send_photo(message.chat.id,row[1])
        bot.send_message(message.chat.id, info, reply_markup=add_to_favorite(row[2],user))
        


def add_to_favorite(id,user):
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Добавить фильм в избранное 🌟", callback_data=json.dumps({'user':user, 'id':id})))
        return markup


def main_markup():
  markup = ReplyKeyboardMarkup()
  markup.add(KeyboardButton('/random'))
  return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = json.loads(call.data)
    manager.add_favorite(data['user'],data['id'])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Hello! You're welcome to the best Movie-Chat-Bot🎥!
Here you can find 1000 movies 🔥
Click /random to get random movie
Or write the title of movie and I will try to find it! 🎬 """, reply_markup=main_markup())

@bot.message_handler(commands=['random'])
def random_movie(message):
    row = manager.get_random_movie()
    self_info(bot, message, row)


@bot.message_handler(commands=['list'])
def list_movie(message):
    con = sqlite3.connect("movie_database.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT title FROM favorite WHERE user_id = {message.chat.id}")
        fav_list = cur.fetchall()
        for i in fav_list:
             bot.send_message(message.chat.id,i)

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,"""Commands:
    /start
    /info
    /random
    /list
    /delete (dont working)
    """)

@bot.message_handler(commands=['delete'])
def del_movie(message):
    con = sqlite3.connect("movie_database.db")
    with con:
         cur = con.cursor()
         cur.execute(f"SELECT title FROM favorite WHERE user_id = {message.chat.id}")
         fav_list = cur.fetchall()
         a = message.text.split('/delete')[1].strip()
         fav_list = [i[0] for i in fav_list]
         if a in fav_list:
              cur.execute(f"DELETE FROM favorite WHERE title = '{a}'")
              bot.send_message(message.chat.id,'Delete is complete')
         else:
              bot.send_message(message.chat.id,'You dont have this movie in favorites')
    
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    con = sqlite3.connect("movie_database.db")
    with con:
        cur = con.cursor()
        cur.execute(f"select * from movies where LOWER(title) = '{message.text.lower()}'")
        row = cur.fetchall()
        if row:
            row = row[0]
            bot.send_message(message.chat.id,"Of course! I know this movie😌")
            self_info(bot, message, row)
        else:
            bot.send_message(message.chat.id,"I don't know this movie ")

        cur.close()



bot.infinity_polling()
