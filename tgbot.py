import base64
from io import BytesIO
from PIL import Image
from telegram import Message, Update, Bot, User
from modules.thonkify_dict import thonkifydict
from telegram.ext import CommandHandler , Updater , MessageHandler , Filters , run_async
import requests
import sqlite3
import sql

TOKEN = '678888523:AAFcp93yAa3--sHokD4Lv9BmfjsjLjw3eR0'

def startmessage(bot , update):
	chat_id = update.message.chat_id
	bot.send_message(chat_id = chat_id , text = '''Greetings! My name is org_manage-bot , I'm here to help 
			you manage you telegram group''' )

def helpbot(bot , update):
	chat_id = update.message.chat_id
	text = '''
	Hey! These are the following commands availaible:
		/start - get started using org-bot
		/senddogphotu - sends a endom dog photo
		/filter - replies to the message when a particular keyword is entered
		/remove - removes the user when you type this in refering to their message
		/thonkify - sends a funny image png when you reply to the message
	'''
	bot.send_message(chat_id = chat_id , text = text)	

def welcome(bot , update):
	chat_id = update.message.chat_id
	text = 'Hello '+update.message.new_chat_members[0].first_name+'! welcome to '+update.message.chat.title+':)'
	bot.send_message(chat_id = chat_id,
		text = text)

def welcome_message(bot, update):
	if update.message.new_chat_members != []:
		return welcome(bot, update)

def sendphoto(bot , update):
	content  = requests.get('https://random.dog/woof.json').json()
	url = content['url']
	chatid = update.message.chat_id
	bot.send_photo(chat_id = chatid , photo = url)

def remove_user(bot , update):
	message = update.effective_message 
	prev_message = message.reply_to_message
	user_id = prev_message.from_user.id
	prev_message.chat.kick_member(user_id)

def extract_effective(text):
	netstr = ''
	for word in text.split(' ')[2:]:
		netstr += word
	return text.split(' ')[1] , netstr

@run_async
def thonkify(bot , update):
	message = update.effective_message 
	msg = message.reply_to_message.text
	print(msg)
	if len(msg) > 39:
		message.reply_text('thonk yourself!');
		return

	tracking = Image.open(BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAYAAAOACAYAAAAZzQIQAAAALElEQVR4nO3BAQ0AAADCoPdPbQ8HFAAAAAAAAAAAAAAAAAAAAAAAAAAAAPwZV4AAAfA8WFIAAAAASUVORK5CYII='))) # base64 encoded empty image(but longer)
	x = 0
	y = 896
	image = Image.new('RGBA', [x, y], (0, 0, 0))
	for character in msg:
		print(character)
		value = thonkifydict.get(character)
		print(value)
		addedimg = Image.new('RGBA', [x + value.size[0] + tracking.size[0], y], (0, 0, 0))
		addedimg.paste(image, [0, 0])
		addedimg.paste(tracking, [x, 0])
		addedimg.paste(value, [x + tracking.size[0], 0])
		image = addedimg	
		x = x + value.size[0] + tracking.size[0]

	maxsize = 1024, 896
	if image.size[0] > maxsize[0]:
		image.thumbnail(maxsize, Image.ANTIALIAS)

	with BytesIO() as buffer:
		buffer.name = 'image.png'
		image.save(buffer, 'PNG')
		buffer.seek(0)
		bot.send_sticker(chat_id=message.chat_id, sticker=buffer)

def filter_resp(bot , update):
	connection = sqlite3.connect("sql/filter.db")
	cursor = connection.cursor()
	chat = update.effective_chat
	msg = update.effective_message.text
	k , r = extract_effective(msg)
	sql_command = """INSERT INTO message (keyword, response)
	VALUES ("{key}" , "{resp}");"""
	sql_command = sql_command.format(key = k , resp = r)
	print(sql_command)
	cursor.execute(sql_command)
	connection.commit()
	connection.close()	
	print('command successfully added!!')

def filter_reply(bot , update):
	print('inside filter_apply')
	connection = sqlite3.connect("sql/filter.db")
	cursor = connection.cursor()
	print(cursor)
	msg = update.effective_message.text
	print(msg)
	for word in msg.split(' ')[1:]:
		cursor.execute("SELECT * FROM message WHERE keyword=?", (word,))
		rows = cursor.fetchall()
		if(len(rows) > 0):
			message = update.effective_message
			message.reply_text(rows[0][1])

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start' ,startmessage))
	dp.add_handler(CommandHandler('senddogphotu' ,sendphoto))
	dp.add_handler(CommandHandler('filter',filter_resp))
	dp.add_handler(CommandHandler('thonkify',thonkify))
	dp.add_handler(CommandHandler('help',helpbot))
	dp.add_handler(CommandHandler('remove',remove_user))
	dp.add_handler(CommandHandler('reply', filter_reply))
	dp.add_handler(MessageHandler([Filters.status_update], welcome_message))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()