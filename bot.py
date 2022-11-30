from config import bot
from time import sleep
import logic
from telebot import types
import re
from database import db
#########################################################
# Aquí vendrá la implementación de la lógica del bot

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)

@bot.message_handler(commands=['menu'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    saludo = "menu creado"
    logic.Createmenu()
    bot.send_message(
        message.chat.id,
        saludo,
        parse_mode="Markdown")
        
@bot.message_handler(commands=['test'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    saludo = ""
    types.InlineKeyboardButton
    print(message.from_user.id)
    if logic.check_admin(message.from_user.id):
        saludo = logic.get_welcome_messageAdmin(bot.get_me())
    else:
        saludo = logic.get_welcome_messageUser(bot.get_me())
    bot.send_message(
        message.chat.id,
        saludo,
        parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def on_command_start(message):
    user_lang(message)
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

def gen_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               types.InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(lambda q: q.data == '/converted')
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")
def user_lang(message):
    try:
        user_lang = message.from_user.language_code.lower()
    except:
        user_lang = 'en-us'
    print(user_lang)

    # i18n.set('fallback', 'en-us')
    set_buttons()


def set_buttons():
    global button
    global button2
    button = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("", callback_data='/send')
    btn2 = types.InlineKeyboardButton("", callback_data='/email')
    button.row(btn1, btn2)
    button2 = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton("", callback_data='/as_is')
    btn4 = types.InlineKeyboardButton("", callback_data='/converted')
    button2.row(btn3, btn4)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())
#########################################################
if __name__ == '__main__':
    bot.infinity_polling()
#########################################################
