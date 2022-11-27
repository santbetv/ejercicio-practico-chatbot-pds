#########################################################
from config import bot
import config
from time import sleep
import re
#########################################################
# Aquí vendrá la implementación de la lógica del bot
@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.send_message(
        message.chat.id,
        "Hola, soy un \U0001F916 de restaurante, ¿cómo estás?",
        parse_mode="Markdown") 

#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################