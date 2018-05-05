from TelegramBot.BaseContext import BaseContext


class OnboardingContext(BaseContext):
    ASKING_NAME = 'asking_name'
    ASKING_EMAIL = 'asking_email'
    ASKING_CALENDAR_AUTH = 'asking_calendar_auth'

    state = None
    is_done_ = False
    local_state = None
    global_event = None

    def __init_(self, event, state):
        self.global_state = state
        self.event = event

    def start(self, bot, chat_id):
        self.local_state = self.ASKING_NAME
        bot.send_message(chat_id=chat_id, text="Please let me know your name so I can address you properly.")

    def process(self, bot, update):
        update.user = self.state.users[update.message.chat_id]
        update.text = update.message.text

        if self.local_state is self.ASKING_EMAIL:
            self.handle_email(update)

        if self.local_state is self.ASKING_NAME:
            self.handle_name(update)

    def handle_email(self, update):
        if "@" not in update.message.text:
            update.message.reply("This does not seem to be an email address")
            return False

        update.user.email = update.text
        update.message.reply("Thanks for your email, the last thing we need is access to your calendar."
                             "Please follow this link: %s", "https://google.com")

        self.local_state = self.ASKING_CALENDAR_AUTH

    def handle_auth(self, update):
        self.is_done_ = True

    def handle_name(self, update):
        update.user.name = update.text
        update.message.reply("Hi %s, welcome to the meeting bot. Please let me also know your email", update.user.name)

        self.local_state = self.ASKING_EMAIL

    def is_done(self):
        return self.is_done_
