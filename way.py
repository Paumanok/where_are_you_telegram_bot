#!/usr/bin/python3

import logging
from requests import get
from io import BytesIO

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram_auth import telegram_auth

class where_are_you:

    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.ta = telegram_auth()
        self.token = self.ta.token

    def update_ip(self):
        self.ip = get('https://api.ipify.org').content.decode('utf8')

    def get_ht_images(self):
        return

    def start(self, update, context):
        #send message when /start is issued
        update.message.reply_text('hello world')

    def help(self, update, context):
        #respond to /help
        update.message.reply_text('ask me where I am')

    def tell_em(self, update, context):
        #tell em of course
        if "here are you" in update.message.text:
            self.update_ip()
            update.message.reply_text(self.ip)
        elif "pdate me" in update.message.text:
            req = get("http://datapaddock.lan:5000/images").content
            
            update.message.reply_photo(photo=req)
        else:
            update.message.reply_text("idk man")


    def error(self, update, context):
        self.logger.warning("update {0} caused error {1}".format(update, context.error))

    def runner(self):
        #start the bot
        #create updater and pass the token
        updater = Updater(self.token, use_context=True)

        #get the dispatcher
        dp = updater.dispatcher

        #add the commands
        dp.add_handler(CommandHandler("start", self.start))

        dp.add_handler(CommandHandler("help", self.help))

        dp.add_handler(MessageHandler(Filters.text, self.tell_em))

        dp.add_error_handler(self.error)

        #start the bot

        updater.start_polling()

        #run the bot until its killed
        updater.idle()



if __name__ == '__main__':
    way = where_are_you()
    way.runner()
