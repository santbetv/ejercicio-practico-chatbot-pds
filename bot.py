from config import bot
from time import sleep
import logic
from telebot import types
import re
from database import db
import json
#########################################################
# Aquí vendrá la implementación de la lógica del bot

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()

if __name__ == '__main__':
    print("main 1 ")
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
    # types.InlineKeyboardButton
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
    # user_lang(message)
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    saludo = ""
    print(message.from_user.id)
    # if logic.check_admin(message.from_user.id):
    saludo = logic.get_welcome_messageAdmin(bot.get_me())
    bot.send_message(message.chat.id, saludo, parse_mode="Markdown")

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton("Gestionar Categorias", callback_data="/Categorias"),
               types.InlineKeyboardButton(
                   "Gestionar Productos", callback_data="/Productos"),
               types.InlineKeyboardButton(
                   "Gestionar Pedidios", callback_data="/Pedidos"),
               types.InlineKeyboardButton("Help", callback_data="/help"))
    print(message.chat.id)
    bot.send_message(
        message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)


@bot.callback_query_handler(func=lambda q: q.data == '/Categorias')
def callback_query(call):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton("listar Categorias", callback_data="/listar_categoria"),
               types.InlineKeyboardButton(
                   "Buscar Categoria", callback_data="/buscar_Categoria"),
               types.InlineKeyboardButton("Editar categoria por id", callback_data="/editar_id"))

    bot.send_message(call.message.chat.id,
                     "Elije la opcon que deseas ver:", reply_markup=markup)
    # print(call)
    # if call.data == '/converted':
    #     # bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
    #     bot.send_message(call.message.chat.id, "Selecciona una opción del menú:", parse_mode="Markdown")
    #     # response = bot.reply_to(call.message, "¿Cuál es producto desea agregar?")
    #     #bot.answer_callback_query(call.id, "Answer is Yes")
    # elif call.data == "help":
    #     bot.answer_callback_query(call.id, "Answer is No")


@bot.callback_query_handler(func=lambda q: q.data == '/listar_categoria')
def callback_query(call):
    Categorias = logic.listar_Categorias()

    text = "Listado de Categorias:\n\n"
    # text = "|Item |Descripción | |- |- | |Problema|<br /> Hoy los negocio se caracterizan por <br />|"

    text += f'| ID | Descripcion | Estado\n'
    for Categoria in Categorias:
        text += f'| {Categoria.id} | {Categoria.descripcion} | {Categoria.estado} \n'

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

    # print(text)


@bot.callback_query_handler(func=lambda q: q.data == '/buscar_Categoria')
def callback_query(call):
    response = bot.reply_to(
        call.message, "¿Por cuál estado quieres filtrar?")
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton("Acivas", callback_data="/list_cat activo"),
               types.InlineKeyboardButton("Inactivos", callback_data="/list_cat inactivo"))

    bot.send_message(call.message.chat.id,
                     "Elije la opcon que deseas ver:", reply_markup=markup)    
    # print(message)
    bot.send_message(call.message.chat.id, "Selecciona una opción del menú:",
                     reply_markup = markup)
    # bot.register_next_step_handler(
    #     response, valorbusqueda)


@ bot.message_handler(regexp = r"^(/list_cat (activo|inactivo))$")
def on_command_imc(message):
    print('buscar_Categoria')
    valorbusqueda(message)


def valorbusqueda(message):
    try:
        print('llego al buscar')
        Categorias=logic.listar_Categorias_X_Estado(message.text)
        print(Categorias)
        text="``` Listado de Categorias:\n\n"
        text += '| ID | Descripcion | Estado\n'
        for Categoria in Categorias:
            # print(json.dumps(Categoria))
            text += f'| {Categoria.id} | {Categoria.descripcion} | {Categoria.estado} \n'
            # text += f"| {account.id} | ${account.balance} |\n"
        text += "```"
        response=bot.reply_to(message, text, parse_mode = "Markdown")
        # bot.register_next_step_handler(response, process_weight_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")
# @bot.message_handler(commands=['imc'])
# def on_command_imc(message):
#     response = bot.reply_to(message, "¿Cuál es tu estatura en metros?")


@ bot.callback_query_handler(func = lambda q: q.data == '/editar_id')
def callback_query(call):
    response = bot.send_message(call.message.chat.id,
                                "¿Por cuál ID quieres filtrar?", parse_mode = "Markdown")

    bot.register_next_step_handler(response, valorbusquedaId)


def valorbusquedaId(message):
    try:
        Categorias=logic.listar_id(message.text)

        text="Listado de Categorias:\n\n"

        text += f'| ID | Descripcion | Estado\n'
        for Categoria in Categorias:
            text += f'| {Categoria.id} | {Categoria.descripcion} | {Categoria.estado} \n'

        response=bot.reply_to(message, text, parse_mode = "Markdown")
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


@ bot.callback_query_handler(func = lambda q: q.data == '/Productos')
def callback_query(call):
    pass


@ bot.callback_query_handler(func=lambda q: q.data == '/Pedidos')
def callback_query(call):
    pass


@ bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call)
    if call.data == '/converted':
        # bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
        bot.send_message(
            call.message.chat.id, "Selecciona una opción del menú:", parse_mode="Markdown")
        # response = bot.reply_to(call.message, "¿Cuál es producto desea agregar?")
        #bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "Answer is No")


@bot.callback_query_handler(lambda q: q.data == '/converted')
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")


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

# @bot.message_handler(func=lambda message: True)
# def message_handler(message):
#     bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())


@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)

    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)


#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
    # bot.infinity_polling()
#########################################################
