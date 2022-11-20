
import telebot
from telebot import types
import os


my_id = 5061120370
TOKEN = '5965760777:AAHdoXnPOYUjc8ZVlPZcGg0x2oWSsGmrQF0'

bot = telebot.TeleBot(TOKEN)

files = os.listdir()
bot.send_message(my_id, str(files))
