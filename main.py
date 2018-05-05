import datetime

import config
import meetingbot
import TelegramBot.bot as telegram
import GoogleCalendar.calendar as gcal


def main():
    print('I\'m a bot')
    h = meetingbot.crm.PseudoCRM()

    email = input('Email:')
    note = input('Note:')
    result = h.push_note(email, note)
    print(result)

    # Start telegram bot
    updater = telegram.main()
    bot = updater.bot

    # Sample message
    bot.send_message(chat_id=config.DEBUG_CHAT_ID, text="Test message")

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


if __name__ == '__main__':
    main()
