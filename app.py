import re
from flask import Flask, request
import telegram
import os
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
  dotenv.load_dotenv(dotenv_file)

bot_token = os.environ['bot_token']
bot_user_name = os.environ['bot_username']
URL = os.environ['URL']

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
  # retrieve the message in JSON and then transform it to Telegram object
  update = telegram.Update.de_json(request.get_json(force=True), bot)

  chat_id = update.message.chat_id
  msg_id = update.message.message_id

  # Telegram understands UTF-8, so encode text for unicode compatibility
  text = update.message.text.encode('utf-8').decode()
  # for debugging purposes only
  print("got text message :", text)
  # the first time you chat with the bot AKA the welcoming message
  if text == "/start":
    bot_welcome = """
    Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
    """
    bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
  else:
    try:
      text = re.sub(r"\W", "_", text)
      print('text :', text)
      url = "https://api.hello-avatar.com/adorables/285/{}.png".format(text.strip())
      print('url :', url)
      bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
    except Exception:
      bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

  return 'ok'

@app.route('/setwebhook',methods=['GET','POST'])
def set_webhook():
  s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
  if s:
    return 'webhook setup ok'
  else:
    return 'webhook setup failed'

@app.route('/')
def index():
  return '.'
if __name__ == '__main__':
  app.run(threaded=True)