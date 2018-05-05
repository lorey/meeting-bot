class BaseContext(object):
    name = None

    def is_done(self):
        raise Exception('implementation missing')

    def process(self, bot, update):
        """
        Processes a given input (update) from the user.
        """
        raise Exception('implementation missing')

    def start(self, bot, chat_id):
        """
        This is how an external trigger starts a context. As such, there is no input.
        """
        raise Exception('implementation missing')
