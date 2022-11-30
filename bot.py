from config import bot
import config
from time import sleep
import logic
import re
#########################################################
# Aquí vendrá la implementación de la lógica del bot


@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    saludo = ""
    print(message.from_user.id)
    if logic.check_admin(message.from_user.id):
        saludo = logic.get_welcome_messageAdmin(bot.get_me())
    else:
        saludo = logic.get_welcome_messageUser(bot.get_me())
    bot.send_message(
        message.chat.id,
        saludo,        
        parse_mode="Markdown")


#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################
