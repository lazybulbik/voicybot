import vosk
import wave
import telebot
from telebot import types
import os
from pydub import AudioSegment
import json


TOKEN = '5965760777:AAHdoXnPOYUjc8ZVlPZcGg0x2oWSsGmrQF0'
folder_with_users = 'data\\'

model = vosk.Model('vosk-model-small-ru-0.22')
rec = vosk.KaldiRecognizer(model, 44100)

bot = telebot.TeleBot(TOKEN)


def recognize_voice(path):
	print('распознование')
	audio = wave.open(path, 'rb')

	while True:
	    data = audio.readframes(44100)
	    if len(data) == 0:
	        break

	    if rec.AcceptWaveform(data):
	        res = json.loads(rec.Result())

	result = json.loads(rec.FinalResult())
	if result['text'] != '':
		return result['text']
	else:
		return 'слова не распознаны..'

@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_message(message.chat.id, 'привет, я помогу тебе перевети бесячие голосовые в текст\nпросто отправь мне голосовое и я пришлю тебе рашифровку')

@bot.message_handler(content_types=['voice'])
def voice(message):
	path = folder_with_users + str(message.message_id) + '.mp3'
	final = folder_with_users + str(message.message_id) + '.wav'

	# скачивание гс
	file_info = bot.get_file(message.voice.file_id)
	downloaded_file = bot.download_file(file_info.file_path)

	with open(path, 'wb') as file:
		file.write(downloaded_file)

	os.system(f'ffmpeg -i {path} {final}')
	os.remove(path)
	print('скачано')

	result = recognize_voice(final)
	bot.reply_to(message, str(result))

	os.remove(final)

try:
	bot.polling()
except:
	pass
