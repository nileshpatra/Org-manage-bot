import base64
from io import BytesIO
from PIL import Image
from telegram import Message, Update, Bot, User
from modules.thonkify_dict import thonkifydict , soc
from telegram.ext import CommandHandler , Updater , MessageHandler , Filters , run_async
import requests
import sqlite3
import sql

#Bot token goes here
TOKEN = ''

#Initial Introduction of the bot
def startmessage(bot , update):
	chat_id = update.message.chat_id
	bot.send_message(chat_id = chat_id , text = '''Greetings! My name is org_manage-bot , I'm here to help 
			you manage you telegram group''' )

#Lists all the commands the bot has
def helpbot(bot , update):
	chat_id = update.message.chat_id
	text = '''
	Hey! These are the following commands availaible:
		/start - get started using org-bot
		/sendlogo - sends the logo of the company
		/addmeeting - add new meting time date and topic
		/next - gives details about the next meeting
		/social - add new social media handle
		/github - gets the github link for the organization
		/facebook - gets the facebook link for the organization
		/website - gets the website link for the organization
		/meetup - gets the meetup link for the organization
		/remove - removes the user when you type this in refering to their message
		/filter - replies to the message when a particular keyword is entered
		/reply - replies to the message if it has been added a 'filter' to
		/thonkify - sends a funny image png when you reply to the message
	'''
	bot.send_message(chat_id = chat_id , text = text)	

# Welcome message when a new user join the group
def welcome(bot , update):
	chat_id = update.message.chat_id
	text = 'Hello '+update.message.new_chat_members[0].first_name+'! welcome to '+update.message.chat.title+':)'
	bot.send_message(chat_id = chat_id,
		text = text)

def welcome_message(bot, update):
	if update.message.new_chat_members != []:
		return welcome(bot, update)

# Unwanted users can be removed via this command
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

# Add new socialmedia handle, organization can ad as many handles as they wish to
def add_socialmedia(bot, update):
	msg = update.effective_message.text
	key , link = extract_effective(msg)
	soc[key.lower()] = link

# Get link of the requested social media handle
def getlink(bot,update):
	message = update.effective_message.text
	key = message[1:]
	chat_id = update.message.chat_id
	if key in soc:
		bot.send_message(chat_id = chat_id, text = soc[key])
	else:
		resp = 'Hander not added yet, to add it type : /social ', key,' <your link>'
		bot.send_message(chat_id = chat_id , text = resp )

# Sends organization logo if present
def sendlogo(bot , update):
	chat_id = update.message.chat_id
	if 'logo' in soc:
		bot.send_photo(chat_id = chat_id , photo = soc['logo'])	
	else:
		resp = 'Hander not added yet, to add it type : /social logo <your link>'
		bot.send_message(chat_id = chat_id , text = 'Hander not added yet, to add it type : /social logo <your link>')

# Used to add a new meeting
def add_meeting(bot,update):
	connection = sqlite3.connect("sql/meetings.db")
	cursor = connection.cursor()
	chat = update.effective_chat
	chat_id = update.message.chat_id
	msg = update.effective_message.text
	_ , date ,time , topic = msg.split(" ")
	sql_command = """INSERT INTO meetup (Date, Time, Topic)
	VALUES ("{date}" , "{time}" , "{topic}");"""
	sql_command = sql_command.format(date = date , time = time , topic = topic)
	cursor.execute(sql_command)
	connection.commit()
	connection.close()	
	bot.send_message(chat_id = chat_id , text = 'command successfully added!')

# Get the latest added meeting
def get_list(bot,update):
	connection = sqlite3.connect("sql/meetings.db")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM meetup;")
	chat_id = update.message.chat_id
	last_row = cursor.fetchall()[-1]
	text = 'Date: '+last_row[0]+' Time: '+last_row[1]+' Topic: '+last_row[2]
	bot.send_message(chat_id = chat_id , text = text)
	connection.close()

# For fun -- A function which sends animated text on command
# I have used some of this code and the thonkify_dict from the skittlesbot code
@run_async
def thonkify(bot , update):
	message = update.effective_message 
	msg = message.reply_to_message.text
	if len(msg) > 39:
		message.reply_text('thonk yourself!');
		return

	tracking = Image.open(BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAYAAAOACAYAAAAZzQIQAAAALElEQVR4nO3BAQ0AAADCoPdPbQ8HFAAAAAAAAAAAAAAAAAAAAAAAAAAAAPwZV4AAAfA8WFIAAAAASUVORK5CYII='))) # base64 encoded empty image(but longer)
	x = 0
	y = 896
	image = Image.new('RGBA', [x, y], (0, 0, 0))
	for character in msg:
		value = thonkifydict.get(character)
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

# Adds a filter - for the bot to respond to the message whenever a valid filter is encountered
def filter_resp(bot , update):
	connection = sqlite3.connect("sql/filter.db")
	cursor = connection.cursor()
	chat = update.effective_chat
	chat_id = update.message.chat_id
	msg = update.effective_message.text
	k , r = extract_effective(msg)
	sql_command = """INSERT INTO message (keyword, response)
	VALUES ("{key}" , "{resp}");"""
	sql_command = sql_command.format(key = k , resp = r)
	cursor.execute(sql_command)
	connection.commit()
	connection.close()
	bot.send_message(chat_id = chat_id , text = 'command successfully added!')

# Responds to the message when a filtered keyword is encountered
def filter_reply(bot , update):
	connection = sqlite3.connect("sql/filter.db")
	cursor = connection.cursor()
	msg = update.effective_message.text
	for word in msg.split(' ')[1:]:
		cursor.execute("SELECT * FROM message WHERE keyword=?", (word,))
		rows = cursor.fetchall()
		if(len(rows) > 0):
			message = update.effective_message
			message.reply_text(rows[0][1])
	connection.close()

def main():
	# Added all the essential command handlers 
	
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start' ,startmessage))
	dp.add_handler(CommandHandler('sendlogo' ,sendlogo))
	dp.add_handler(CommandHandler('addmeeting' ,add_meeting))
	dp.add_handler(CommandHandler('next' ,get_list))
	dp.add_handler(CommandHandler('filter',filter_resp))
	dp.add_handler(CommandHandler('reply',filter_reply))
	dp.add_handler(CommandHandler('thonkify',thonkify))
	dp.add_handler(CommandHandler('help',helpbot))
	dp.add_handler(CommandHandler('social',add_socialmedia))
	dp.add_handler(CommandHandler('remove',remove_user))
	dp.add_handler(CommandHandler('facebook', getlink))
	dp.add_handler(CommandHandler('github', getlink))
	dp.add_handler(CommandHandler('website', getlink))
	dp.add_handler(CommandHandler('meetup', getlink))
	dp.add_handler(MessageHandler([Filters.status_update], welcome_message))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
