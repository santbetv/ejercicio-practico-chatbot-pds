from config import bot
from time import sleep
import logic
from telebot import types
import re
from database import db
from models.ItemCategoria import ItemCategoria
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
    db.Base.metadata.create_all(db.engine)

bot_data = {}


# class Record:
#     def __init__(self):
#         self['idcateditar'] = None
#         self.itemcategoria = {}


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
                   "Filtrar Categoria", callback_data="/buscar_Categoria"),
               types.InlineKeyboardButton(
                   "Editar categoria por id", callback_data="/editar_Categoria_id"),
               types.InlineKeyboardButton(
                   "Agragar Categoria", callback_data="/agregar_categoria"))

    bot.send_message(call.message.chat.id,
                     "Elije la opcion que deseas ver:", reply_markup=markup)
    # print(call)
    # if call.data == '/converted':
    #     # bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
    #     bot.send_message(call.message.chat.id, "Selecciona una opción del menú:", parse_mode="Markdown")
    #     # response = bot.reply_to(call.message, "¿Cuál es producto desea agregar?")
    #     #bot.answer_callback_query(call.id, "Answer is Yes")
    # elif call.data == "help":
    #     bot.answer_callback_query(call.id, "Answer is No")


@bot.callback_query_handler(func=lambda q: q.data == '/Productos')
def callback_query(call):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton(
        "Listar Platos", callback_data="/listar_plato"),
        types.InlineKeyboardButton("Agragar Plato", callback_data="/agregar_plato"))

    bot.send_message(call.message.chat.id,
                     "Elije la opcion que deseas ver:", reply_markup=markup)


@bot.callback_query_handler(func=lambda q: q.data == '/listar_categoria')
def callback_query(call):
    Categorias = logic.listar_Categorias()
    text = logic.getMessageCategorias(Categorias)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    # print(text)


@bot.callback_query_handler(func=lambda q: q.data == '/agregar_categoria')
def callback_query(call):
    text = "Ingresa la descripcion de la nueva categoria"
    response = bot.send_message(
        call.message.chat.id, text)
    bot.register_next_step_handler(response, guardarCategoria)


def guardarCategoria(message):
    if logic.Guardarcategoria(message.text):
        bot.send_message(message.chat.id,
                         "Se ha guardado correctamente correctamente")


@bot.callback_query_handler(func=lambda q: q.data == '/buscar_Categoria')
def callback_query(call):
    response = bot.reply_to(
        call.message, "¿Por cuál estado quieres filtrar?")
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton("Acivas", callback_data="/list_catactivo"),
               types.InlineKeyboardButton("Inactivos", callback_data="/list_catinactivo"))

    bot.send_message(call.message.chat.id,
                     "Elije la opcion que deseas ver:", reply_markup=markup)
    # bot.register_next_step_handler(
    #     response, valorbusqueda)


@ bot.callback_query_handler(func=lambda q: q.data == '/list_catactivo')
def on_command_ListActivo(call):
    Categorias = logic.listar_Categorias_X_Estado(True)
    text = logic.getMessageCategorias(Categorias)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


@ bot.callback_query_handler(func=lambda q: q.data == '/list_catinactivo')
def on_command_Inactivo(call):
    Categorias = logic.listar_Categorias_X_Estado(False)
    text = logic.getMessageCategorias(Categorias)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


@ bot.callback_query_handler(func=lambda q: q.data == '/editar_Categoria_id')
def callback_query(call):
    response = bot.send_message(call.message.chat.id,
                                "¿Cuál ID quieres editar?")

    bot.register_next_step_handler(response, Editarcategoria)


@bot.callback_query_handler(func=lambda q: q.data == '/listar_plato')
def callback_query(call):
    items = logic.listar_Categorias_itemCategorias()
    print(items)
    text = logic.getMessageCategoriasItems(items)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda q: q.data == '/agregar_plato')
def callback_query(call):
    response = bot.send_message(call.message.chat.id, "Nombre plato?")
    bot.register_next_step_handler(response, NombrePlato)


""" Metodos-------------------------------------------------------------------------"""


def NombrePlato(message):
    try:
        bot_data[message.chat.id] = {}
        bot_data[message.chat.id]['itemcategoria'] = {}
        bot_data[message.chat.id]['itemcategoria']['nombre'] = message.text
        response = bot.reply_to(message, '¿Indique descripcion del plato')
        bot.register_next_step_handler(response, ValidarDescripcion)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def ValidarDescripcion(message):
    try:
        bot_data[message.chat.id]['itemcategoria']['descripcion'] = message.text
        response = bot.reply_to(message, '¿Indique el precio?')
        bot.register_next_step_handler(response, ValidarPrecio)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def ValidarPrecio(message):
    try:
        bot_data[message.chat.id]['itemcategoria']['precio'] = message.text
        response = bot.reply_to(
            message, '¿Indique el id de la categoria a la que desea asociar el producto?')
        bot.register_next_step_handler(response, ValidarcategoriaProd)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def ValidarcategoriaProd(message):
    try:
        bot_data[message.chat.id]['itemcategoria']['IdCategoria'] = message.text
        GuardarPlatos(message)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def GuardarPlatos(message):
    if logic.GuardarPlatos(bot_data[message.chat.id]['itemcategoria']):
        bot.send_message(
            message.chat.id, "Se ha guardado el plato correctamente correctamente")


def Editarcategoria(message, id=None):
    try:
        if id == None:
            id = message.text
        Categorias = logic.listar_id(id)
        text = logic.getMessageCategorias(Categorias)
        bot.reply_to(message, text, parse_mode="Markdown")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Descripcion', 'Estado')

        response = bot.send_message(message.chat.id,
                                    "Elije el campo que deseas editar", reply_markup=markup)
        bot_data[message.chat.id] = {}
        bot_data[message.chat.id]['idcateditar'] = id

        bot.register_next_step_handler(
            response, EditarcategoriaXtipo)

    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def EditarcategoriaXtipo(message):
    try:
        if message.text == 'Descripcion':
            response = bot.send_message(message.chat.id,
                                        "Escribe el nuevo valor de la descripcion")
            bot.register_next_step_handler(
                response, EditarcategoriaDescripcion)
        elif message.text == 'Estado':
            if logic.EditarCategoria(bot_data[message.chat.id]['idcateditar'], message.text, message.text):
                bot.send_message(message.chat.id,
                                 "Se ha editado el estado correctamente")
        else:
            bot.send_message(message.chat.id,
                             "no has seleccionado una opcion valida")
            Editarcategoria(message, bot_data[message.chat.id]['idcateditar'])
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió donde pensamos: {e}")


def EditarcategoriaDescripcion(message):
    if logic.EditarCategoria(bot_data[message.chat.id]['idcateditar'], "Descripcion", message.text):
        bot.send_message(message.chat.id,
                         "Se ha editado la descripcion correctamente")


def EditarcategoriaEstado(message):
    pass


@ bot.callback_query_handler(func=lambda q: q.data == '/Productos')
def callback_query(call):
    pass


@ bot.callback_query_handler(func=lambda q: q.data == '/Pedidos')
def callback_query(call):
    pass


@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)

    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)


#########################################################
if __name__ == '__main__':
    # bot.polling(timeout=20)
    bot.infinity_polling()
#########################################################
