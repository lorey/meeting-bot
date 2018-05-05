import TelegramBot.bot as telegram
import os


def main():
    print('I\'m a bot')

    # Start telegram bot
    updater = telegram.main()
    bot = updater.bot

    # Sample message
    bot.send_message(chat_id=os.environ["DEBUG_CHAT_ID"], text="Test message")

    # Keep the process alive
    updater.idle()


if __name__ == '__main__':
    main()
