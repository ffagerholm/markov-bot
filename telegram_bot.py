#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import markovify
from markov_model import POSifiedText
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, 
                     text="Write anything to get a response!")

def response(bot, update):
    bot.send_message(chat_id=update.message.chat_id, 
                     text=model.make_short_sentence(120))


def run_bot():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    response_handler = MessageHandler(Filters.text, response)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(response_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    with open('data/model.json', 'r') as f:
        model_json = f.read()

    # generate Markov model
    model = POSifiedText.from_json(model_json)
    run_bot()
