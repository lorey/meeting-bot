import datetime
import logging

import TelegramBot.bot as telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import googlecalendar
import config
import meetingbot


class State(object):
    _updater = None
    _crm = None
    _event = None
    _chat_id = None

    def __init__(self, updater, crm):
        self._updater = updater
        self._crm = crm
        self._event = None

    def start(self, bot: telegram.Bot, update: telegram.Update):
        print('User %s has started the bot' % update.effective_user)
        self._chat_id = update.message.chat_id

    def help(self, bot: telegram.Bot, update: telegram.Update):
        print('User %s needs help' % update.effective_user)

    def log(self, bot: telegram.Bot, update: telegram.Update):
        print('User %s wants to log' % update.effective_user)
        email = ''
        note = ''
        self._crm.push_note(email, note)

    def meeting_notifier(self, bot, job):
        # todo make sure that there is no current dialogue
        # todo fetch events
        # todo check if event is ending within next minute
        # todo open new dialogue that asks if you want to create a note
        event = googlecalendar.next_meeeting()

        if event and event['attendees']:
            event_name = event['summary']
            text = 'Your last event was "%s". Please enter your notes:' % event_name
            bot.send_message(chat_id=self._chat_id, text=text)

    def receive(self, bot, update: telegram.Update):
        if not self._event:
            bot.send_message(chat_id=self._chat_id, text='No event set')
            return

        event = self._event
        event_name = event['summary']
        attendees = [att['email'] for att in event['attendees']]
        email = attendees[0]

        message = update.message

        self._crm.push_note(email, message.text)
        bot.send_message(chat_id=self._chat_id, text='Your note on "%s" has been saved at %s.' % (event_name, email))

        # unset event to avoid errors
        self._event = None


def main():
    googlecalendar.setup(1234)

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
    dp.add_handler(MessageHandler(Filters.all, state.receive))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    bot = updater.bot

    # Keep the process alive
    updater.idle()

    # schedule calendar checks
    interval = datetime.timedelta(seconds=60)
    updater.job_queue.run_repeating(state.meeting_notifier, interval, first=0)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    main()
