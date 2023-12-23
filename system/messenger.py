import configparser
import os

from telethon.sync import TelegramClient

from system.logs import logger

config = configparser.ConfigParser()
config.read("./config.ini")
bot_token = (config["bot"]["bot_token"])
api_id = int(config["bot"]["api_id"])
api_hash = (config["bot"]["api_hash"])
notification_to = (config["bot"]["notification_to"])
notification_to = [telegram_id for telegram_id in notification_to.split(',')]


class Messenger(object):
    """Singleton"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Messenger, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'bot'):
            self.bot = TelegramClient(os.path.join('sessions', 'bot_messanger'), api_id, api_hash).start(bot_token=bot_token)

    def send_message_to_telegram(self, message: str):
        for admin in notification_to:
            self.bot.send_message(admin, message)


if __name__ == '__main__':

    # testing
    messenger = Messenger()
    messenger.send_message_to_telegram('test')
