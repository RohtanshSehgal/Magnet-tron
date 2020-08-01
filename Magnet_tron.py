#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""

import json
import requests

# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters


def start(update, context):
    update.message.reply_text('Hi!,Enter what youll like to download (please be specific :-) )!!!')


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))


def help_command(update, context):
    update.message.reply_text("Use /start to test this bot.")


def torr_bot(update, context):
    class Processing:
        def __init__(self, name, size, type, link, mlink):
            self.name = name
            self.size = size
            self.type = type
            self.link = link
            self.m_link = mlink

        def result(self):
            return f"NAME::{self.name}\nSIZE::{self.size}\nTYPE::{self.type}"

    search = update.message.text
    url = "https://api.sumanjay.cf/torrent/?query="
    r = requests.get(url + search)
    answer = r.text
    jsondata = json.loads(answer)
    i = 0
    data = []
    for item in jsondata:
        final = Processing(item["name"], item["size"],item["type"], item["url"], (item["magnet"]))
        if item["age"] <= "10 years" and item["nsfw"] != True:
            final = Processing(item["name"], item["size"],item["type"], item["url"], (item["magnet"]))
            i = i + 1
            if i <= 10:
                update.message.reply_text(final.result())

                keyboard = [[InlineKeyboardButton("URL(open using vpn)", url=final.link)],
                            [InlineKeyboardButton("MAGNETIC(it will directly open in clipboard)",
                                                  switch_inline_query_current_chat=final.m_link)],
                            [InlineKeyboardButton("MAGNETIC(choose if you want to send magnet to other chat)",
                                                  switch_inline_query=final.m_link)]]

                update.message.reply_text('MAGNET LINK IS:', reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                pass


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1226796937:AAFQzqujQAlnr8TWk3gGdk4F8kfc4b93J4E", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, torr_bot))
    updater.dispatcher.add_handler(CallbackQueryHandler(button, torr_bot))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()


