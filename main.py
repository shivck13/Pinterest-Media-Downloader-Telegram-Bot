# -*- coding: utf-8 -*-

from telegram.ext import filters, Updater, CommandHandler, MessageHandler, RegexHandler
import validators
import mimetypes
import os
from pinterest_media_downloader import PinterestMediaDownloader

# initialisation
mimetypes.init()
TOKEN = os.environ['BOT_TOKEN']
updater = Updater(token=TOKEN, use_context=True)

# Actions
def handle_start(update, context):
	start_info = '''
	<b>😃👋 Hi There!\nI'm a Pinterest Media Downloader bot!</b>
\n\nI can help you download images and videos from Pinterest posts!
	'''
	context.bot.send_message(chat_id=update.effective_chat.id, text=start_info, parse_mode='HTML')
	handle_help(update, context)

def handle_help(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="😊 Just send me a Pin link and see the magic! 🪄", parse_mode='HTML')

def handle_links(update, context):
  pin_link = update.message.text.strip()
  if validators.url(pin_link):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🙂 Please wait! I'm working on it!", parse_mode='HTML')
    
    try:
      pmd = PinterestMediaDownloader(pin_link)
      pmd.run()
      
      for media in pmd.best_sizes:
        type = mimetypes.guess_type(media["url"].strip())[0].split("/")[0]
        if type == "image":
          context.bot.send_photo(chat_id=update.effective_chat.id, photo=media["url"])
        elif type == "video":
          context.bot.send_video(chat_id=update.effective_chat.id, video=media["url"])
        else:
          context.bot.send_message(chat_id=update.effective_chat.id, text="🙄 Invalid media type found!", parse_mode='HTML')
    except:
      context.bot.send_message(chat_id=update.effective_chat.id, text="😔 I'm sorry! Either the link was not correct or some other error occurred!")
    else:
      context.bot.send_message(chat_id=update.effective_chat.id, text="😅 All available media downloaded!")
    
  else:
    context.bot.send_message(chat_id=update.effective_chat.id, text="😬 Sorry that's not a link!\nSend me only the Pin links from Pinterest.", parse_mode='HTML')

def handle_unknown(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="😢 Sorry, I didn't understand that.\nI'll ask my developer to make me smarter! 😎")
	handle_help(update, context)

def handle_bye(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Ok Bye!\nHope to see you again!")


  
# Command Handling
updater.dispatcher.add_handler(CommandHandler('start', handle_start))
updater.dispatcher.add_handler(CommandHandler('help', handle_help))
updater.dispatcher.add_handler(CommandHandler('end', handle_bye))

# Message Handling 
updater.dispatcher.add_handler(MessageHandler(filters.Filters.text, handle_links))

#unknown commands
updater.dispatcher.add_handler(MessageHandler(filters.Filters.all, handle_unknown))

# Execute
print('Bot is running...')
updater.start_polling()
updater.idle()
#updater.stop()
