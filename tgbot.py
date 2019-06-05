from telegram.ext import CommandHandler , Updater , MessageHandler , Filters
import requests

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
	chat = update.effective_chat
	user = update.effective_user  
	message = update.effective_message 
	prev_message = message.reply_to_message
	user_id = prev_message.from_user.id
	prev_message.chat.kick_member(user_id)

def extract_effective(text):
	netstr = ''
	for word in text.split(' ')[2:]:
		netstr += word
	return netstr

def filter_resp(bot , update):
	chat = update.effective_chat
	msg = update.effective_message

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start' ,startmessage))
	dp.add_handler(CommandHandler('senddogphotu' ,sendphoto))
	dp.add_handler(CommandHandler('filter',filter_resp))
	dp.add_handler(CommandHandler('help',helpbot))
	dp.add_handler(CommandHandler('remove',remove_user))
	dp.add_handler(MessageHandler([Filters.status_update], welcome_message))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()