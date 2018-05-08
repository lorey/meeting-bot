import datetime
import logging


import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler, CallbackQueryHandler

import config
import googlecalendar
import meetingbot

CALENDAR_CHECK_INTERVAL = 120

CHOOSING, MEETING, LOCATION, BIO = range(4)

class State(object):
    _updater = None
    _crm = None
    _event = None
    _chat_id = None

    def __init__(self, updater, crm):
        self._updater = updater
        self._crm = crm
        self._event = None

    def start(self, bot, update, job_queue):
        print('User %s has started the bot' % update.effective_user)
        self._chat_id = update.message.chat_id
        interval = datetime.timedelta(seconds=CALENDAR_CHECK_INTERVAL)
        job_queue.run_repeating(self.meeting_notifier, interval, first=0, context=update)

        # return MEETING
        

    def help(self, bot, update):
        print('User %s needs help' % update.effective_user)

    def log(self, bot, update):
        print('User %s wants to log' % update.effective_user)
        email = ''
        note = ''
        self._crm.push_note(email, note)

    def meeting_notifier(self, bot, job):
        # todo make sure that there is no current dialogue
        # todo fetch events
        # todo check if event is ending within next minute
        # todo open new dialogue that asks if you want to create a note
        event = googlecalendar.next_meeeting(20000)

        if event and self._chat_id:
            if 'attendees' in event:
                

                event_name = event['summary']
                waving_hand = u'\U0001F44B'
                text = 'Hi there ' + waving_hand
                bot.send_message(chat_id=self._chat_id, text=text)
                
                # print(bot)
                # print(job.updater.update)
                update = job.context
                text = 'I just saw you finished a meeting. the title suggests it was about "%s"' % event_name
                bot.send_message(chat_id=self._chat_id, text=text)

                # reply_keyboard = [['Yes, sure Thing!', 'No, not now']]
                keyboard = [[InlineKeyboardButton("Yes, sure Thing!", callback_data='yes'),
                        InlineKeyboardButton("No, not now", callback_data='no')],
                        [InlineKeyboardButton("Someone else is doing it", callback_data='other')]]

                reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

                update.message.reply_text(
                    'Do you have a few seconds to answer some questions regarding this meeting?',
                    reply_markup=reply_markup
                )
                # print('lalallala')
                # bot.update
                # return CHOOSING

            else:
                logging.info('Skipping event without attendees: %s' % event)

    def receive(self, bot, update):
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

    def button(self, bot, update):
        query = update.callback_query
        
        # TODO: Save user data

        if query.data == 'yes':
            self.query_overall(bot,update)
        elif query.data == 'no':
            self.remind_me_later(bot,update)
        elif query.data == 'other':
            bot.send_message(chat_id=self._chat_id, text='Who?')
        elif query.data == '30min':
            bot.send_message(chat_id=self._chat_id, text='Ok, i will remind you in 30 minutes')
        elif query.data == '60min':
            bot.send_message(chat_id=self._chat_id, text='Ok, i will remind you in 60 minutes')
        elif query.data == 'tonight':
            bot.send_message(chat_id=self._chat_id, text='Ok, i will remind you tonight')
        elif query.data == 'custom':
            bot.send_message(chat_id=self._chat_id, text='Ok, When does it suit you better')
        elif query.data in '0123456789':
            self.query_success(bot,update)
        elif 'success' in query.data:
            self.query_prepared(bot,update)
        elif 'prepared' in query.data:
            self.write_note(bot,update)
        elif query.data == 'noteYes':
            note = update.message.text
            email = ''
            self._crm.push_note(email, note)



    def remind_me_later(self, bot, update):
        print('User %s wants to do the quiz later' % update.effective_user)
        
        keyboard = [[InlineKeyboardButton("30 min", callback_data='30min'), InlineKeyboardButton("60 min", callback_data='60min')],
                    [InlineKeyboardButton("tonight", callback_data='tonight'),InlineKeyboardButton("Custom...", callback_data='custom')]]

        reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

        bot.send_message(chat_id=self._chat_id,text='Ok. When should I remind you next?',reply_markup=reply_markup )



    def query_overall(self, bot, update):
        # print('User %s wants to do the query now' % update.effective_user)
        strong_arm = u'\U0001F4AA'
        bot.send_message(chat_id=self._chat_id, text='Perfet. Lets start ' + strong_arm)

        keyboard_overall = [[InlineKeyboardButton("1", callback_data='1'), InlineKeyboardButton("2", callback_data='2')],
                            [InlineKeyboardButton("3", callback_data='3'), InlineKeyboardButton("4", callback_data='4')],
                            [InlineKeyboardButton("5", callback_data='5'), InlineKeyboardButton("6", callback_data='6')],
                            [InlineKeyboardButton("7", callback_data='7'), InlineKeyboardButton("8", callback_data='8')],
                            [InlineKeyboardButton("9", callback_data='9'), InlineKeyboardButton("10", callback_data='10')]]

        reply_markup_overall = InlineKeyboardMarkup(keyboard_overall, one_time_keyboard=True)

        bot.send_message(
            chat_id=self._chat_id,
            text='On a scale from 1 to 10. How is your overall feeling of the meeting?',
            reply_markup=reply_markup_overall
        )


    def query_success(self, bot, update):
        keyboard_success = [[InlineKeyboardButton("Yes", callback_data='successYes'), InlineKeyboardButton("No", callback_data='successNo')],
                            [InlineKeyboardButton("Hard to Tell", callback_data='successUndecided')]]
        
        reply_markup_success = InlineKeyboardMarkup(keyboard_success, one_time_keyboard=True)


        bot.send_message(
            chat_id=self._chat_id,
            text='Was the meeting a success?',
            reply_markup=reply_markup_success
        )


    def query_prepared(self, bot, update):
        keyboard_prepared = [[InlineKeyboardButton("Yes", callback_data='preparedYes'), InlineKeyboardButton("No", callback_data='preparedNo')]]
        reply_markup_prepared = InlineKeyboardMarkup(keyboard_prepared, one_time_keyboard=True)
       
        bot.send_message(
            chat_id=self._chat_id,
            text='Where you sufficiently prepared?',
            reply_markup=reply_markup_prepared
        )

    def write_note(self, bot, update): 
        nerd_face = u'\U0001F913' 
        bot.send_message(
            chat_id=self._chat_id,
            text='Last but not least its time to write the note. I know this is tedious, but non the less super important ' + nerd_face
        )

        bot.send_message(
            chat_id=self._chat_id,
            text='Just drop a few lines and do the full note later.'
        )


    def send_note(self, bot, update):
        user_text = update.message.text
        
        keyboard_note = [[InlineKeyboardButton("Yes", callback_data='noteYes'), InlineKeyboardButton("No", callback_data='noteNo')]]
        reply_markup_note = InlineKeyboardMarkup(keyboard_note, one_time_keyboard=True)
        bot.send_message(
            chat_id=self._chat_id,
            text='Is this the note you want send to our CRM?\n\n' + user_text,
            reply_markup=reply_markup_note
        )
        



def main():
    logging.basicConfig(level=logging.INFO)
    googlecalendar.setup()

    #
    # Start telegram bot
    #
    updater = Updater(config.TELEGRAM_TOKEN)

    crm = meetingbot.crm.PseudoCRM()
    state = State(updater, crm)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", state.start, pass_job_queue=True))
    dp.add_handler(CommandHandler("help", state.help))
    dp.add_handler(CommandHandler('log', state.log))
    dp.add_handler(MessageHandler(Filters.text, state.send_note))
    updater.dispatcher.add_handler(CallbackQueryHandler(state.button))
    # dp.add_handler(RegexHandler('^(Yes, sure Thing!)$', state.short_query))
    # dp.add_handler(RegexHandler('^(No, not now)$', state.remind_me_later))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', state.start)],

    #     states={

    #         CHOOSING: [RegexHandler('^(Yes, sure thing)$', state.short_query, pass_user_data=True), 
    #                    RegexHandler('^(No, not now)$',state.remind_me_later)],

            # PHOTO: [MessageHandler(Filters.photo, state.short_query),
            #         CommandHandler('skip', state.remind_me_later)],

    #         LOCATION: [MessageHandler(Filters.location, location),
    #                    CommandHandler('skip', skip_location)],

    #         BIO: [MessageHandler(Filters.text, bio)]
    #     },

    #     fallbacks=[CommandHandler('log', state.log)]
    # )

    # dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    bot = updater.bot

    # schedule calendar checks
    # interval = datetime.timedelta(seconds=CALENDAR_CHECK_INTERVAL)
    # updater.job_queue.run_repeating(state.meeting_notifier, interval, first=0, context=updater)

    # Keep the process alive
    updater.idle()

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    main()
