# Org-manage-bot

- This is a telegram bot which an organization can use to manage their group.
- It has the following features:
  - Schedule a meeting
  - Know the latest meeting
  - Get all the social media accounts in one go
  - Send company Logo
  - Add new handles and logos
  - Remove user
  - Filter a particular keyword and replies to the keyword when it finds that
  - Get replies whenever filtered text is encountered
  - Get Animated version of text on calling thonkify (Some of the code has been referred from skittlesbot)
  
# Testing the bot

- In order to test the bot, generate a token for your own bot with botfather
- Copy-Paste the token that you were allotted inside the TOKEN='' variable in tgbot.py file
	- For instance if the token generated is xyz, you should replace TOKEN='xyz'
- Do refer to [this](https://www.freecodecamp.org/news/learn-to-build-your-first-bot-in-telegram-with-python-4c99526765e4/) link to create your own instances of bots, and test the code.

# To run in development mode:

- First make a virtual environment with: `virtualenv -p python3 <name_for_virtualenv>`
- Activate the virtualenv with `source <name_of_virtualenv>/bin/activate`
- Now, install the requirements using `pip3 install -r requirements.txt`
- You are good to go! Directly run the script with:
 	```
 	python3 tgbot.py
 	```
[Here](https://youtu.be/xiI_u60Vrq0) is a video detailing the setup
