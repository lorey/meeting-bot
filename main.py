import datetime
import logging

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

import config
import meetingbot


class State(object):
    _updater = None
    _crm = None

    def __init__(self, updater, crm):
        self._updater = updater
        self._crm = crm

    def start(self, bot: telegram.Bot, update: telegram.Update):
        print('User %s has started the bot' % update.effective_user)

    def help(self, bot: telegram.Bot, update: telegram.Update):
        print('User %s needs help' % update.effective_user)

    def log(self, bot: telegram.Bot, update: telegram.Update):
        print('User %s wants to log' % update.effective_user)
        email = ''
        note = ''
        self._crm.push_note(email, note)


def main():
    #
    # Start telegram bot
    #
    updater = Updater(config.TELEGRAM_TOKEN)

    crm = meetingbot.crm.PseudoCRM()
    state = State(updater, crm)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", state.start))
    dp.add_handler(CommandHandler("help", state.help))
    dp.add_handler(CommandHandler('log', state.log))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    bot = updater.bot

    # Keep the process alive
    updater.idle()

    # schedule calendar checks
    interval = datetime.timedelta(seconds=60)
    updater.job_queue.run_repeating(meeting_notifier, interval, first=0)


def meeting_notifier(bot, job):
    # todo make sure that there is no current dialogue
    # todo fetch events
    # todo check if event is ending within next minute
    # todo open new dialogue that asks if you want to create a note
    bot.send_message(chat_id=config.DEBUG_CHAT_ID, text='Checking your calendar')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    main()
