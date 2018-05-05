import config
import meetingbot
import TelegramBot.bot as telegram


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
    bot.send_message(chat_id=config["DEBUG_CHAT_ID"], text="Test message")

    # Keep the process alive
    updater.idle()


if __name__ == '__main__':
    main()
