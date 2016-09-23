__author__ = 'antonioirizar'
from twx.botapi import TelegramBot, ReplyKeyboardMarkup, Error
from user import User


class Botonio:
    def __init__(self, token):
        self.users = {}
        self.bot = TelegramBot(token)
        self.bot.update_bot_info().wait()
        self.offset = 1
        updates = self.bot.get_updates().wait()
        if isinstance(updates, Error):
            print(updates)
            raise Exception('Error to conect with Telegram.')
        if len(updates):
            self.offset = updates[-1].update_id

    def start(self):
        while True:
            updates = self.bot.get_updates(offset=self.offset).wait()
            if not len(updates):
                continue
            self.offset = updates[-1].update_id
            self.offset += 1
            for update in updates:
                if update.message is None:
                    continue
                sender = update.message.sender
                if sender.id not in self.users:
                    user = User(sender.first_name, sender.id)
                    self.users[user.user_id] = user
                else:
                    user = self.users[sender.id]
                if update.message.text == 'stop':
                    del self.users[user]
                    continue
                messages = user.process_message(update.message.text)
                if isinstance(messages, tuple):
                    self.bot.send_message(user.user_id, messages[0], reply_markup=self._numeric_keyboard()).wait()
                else:
                    self.bot.send_message(user.user_id, messages).wait()

    @staticmethod
    def _numeric_keyboard():
        keyboard = [
            ['1', '2'],
            ['3', '4']
        ]
        return ReplyKeyboardMarkup.create(keyboard)
