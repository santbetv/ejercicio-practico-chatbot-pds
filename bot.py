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


@bot.message_handler(commands=['test'])
def on_command_test(message):
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
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    saludo = ""
    # print(message.from_user.id)
    # if logic.check_admin(message.from_user.id):
    saludo = logic.get_welcome_messageAdmin(bot.get_me())
    bot.send_message(message.chat.id, saludo, parse_mode="Markdown")
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Gestionar Categorias", callback_data="/Categorias"),
               types.InlineKeyboardButton(
                   "Gestionar Productos", callback_data="/Productos"),
               types.InlineKeyboardButton(
                   "Gestionar Pedidios", callback_data="/Pedidos"),
               types.InlineKeyboardButton("Help", callback_data="/help"))
    bot.send_message(
        message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)

# --------------------Inicio Categorias


@bot.callback_query_handler(func=lambda q: q.data == '/Categorias')
def callback_query_categorias(call):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton("Listar Categorias", callback_data="/listar_categorias"),
               types.InlineKeyboardButton(
                   "Filtrar Categoria", callback_data="/buscar_Categoria"),
               types.InlineKeyboardButton(
                   "Editar categoria por id", callback_data="/editar_Categoria_id"),
               types.InlineKeyboardButton(
                   "Agragar Categoria", callback_data="/agregar_categoria"))
    bot.send_message(call.message.chat.id,
                     "Elije la opción que deseas ver:", reply_markup=markup)


@bot.callback_query_handler(func=lambda q: q.data == '/listar_categorias')
def callback_query_listar_categorias(call):
    Categorias = logic.listar_Categorias()
    text = logic.getMessageCategorias(Categorias)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    # print(text)


@bot.callback_query_handler(func=lambda q: q.data == '/agregar_categoria')
def callback_query_agregar_categoria(call):
    text = "Ingresa la descripción de la nueva categoria"
    response = bot.send_message(
        call.message.chat.id, text)
    bot.register_next_step_handler(response, guardarCategoria)


def guardarCategoria(message):
    if logic.Guardarcategoria(message.text):
        bot.send_message(message.chat.id,
                         "Se ha guardado correctamente correctamente")


@bot.callback_query_handler(func=lambda q: q.data == '/buscar_Categoria')
def callback_query_buscar_categoria(call):
    bot.reply_to(
        call.message, "¿Por cuál estado quieres filtrar?")
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Acivas", callback_data="/list_catactivo"),
               types.InlineKeyboardButton("Inactivas", callback_data="/list_catinactivo"))
    bot.send_message(call.message.chat.id,
                     "Elije la opción que deseas ver:", reply_markup=markup)


@bot.callback_query_handler(func=lambda q: q.data == '/list_catactivo')
def on_command_ListCatActivo(call):
    Categorias = logic.listar_Categorias_X_Estado(True)
    text = logic.getMessageCategorias(Categorias)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda q: q.data == '/list_catinactivo')
def on_command_ListCatInactivo(call):
    Categorias = logic.listar_Categorias_X_Estado(False)
    text = logic.getMessageCategorias(Categorias)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda q: q.data == '/editar_Categoria_id')
def callback_query_editar_categoria_id(call):
    response = bot.send_message(call.message.chat.id,
                                "¿Cuál ID quieres editar?")
    bot.register_next_step_handler(response, Editarcategoria)
# ---------------end categorias
# --------------Inicio Productos


@bot.callback_query_handler(func=lambda q: q.data == '/Productos')
def callback_query(call):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton("Listar Platos", callback_data="/listar_platos"),
               types.InlineKeyboardButton(
                   "Agragar Plato", callback_data="/agregar_plato"),
               types.InlineKeyboardButton("Editar Platos", callback_data="/Editar_plato"))

    bot.send_message(call.message.chat.id,
                     "Elije la opción que deseas ver:", reply_markup=markup)


@bot.callback_query_handler(func=lambda q: q.data == '/listar_platos')
def callback_query_listar_platos(call):
    items = logic.listar_Categorias_itemCategorias()
    text = logic.getMessageCategoriasItems(items)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda q: q.data == '/agregar_plato')
def callback_query_agregar_plato(call):
    response = bot.send_message(call.message.chat.id, "Nombre plato?")
    bot.register_next_step_handler(response, NombrePlato)

@ bot.callback_query_handler(func=lambda q: q.data == '/Editar_plato')
def callback_query(call):
    response = bot.send_message(call.message.chat.id,
                                "¿Cuál ID quieres editar?")

    bot.register_next_step_handler(response, Editarcategoria)

@bot.callback_query_handler(func=lambda q: q.data == '/edita_estado_pedido')
def callback_query_editar_producto(call):
    response = bot.send_message(call.message.chat.id, "¿Indica el ID del pedido?")
    bot.register_next_step_handler(response, indicarIdPedido)

# --------------end Productos
# ---------------Inicio Pedidos
@bot.callback_query_handler(func=lambda q: q.data == '/Pedidos')
def callback_query_pedidos(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    logic.pintarBotones(markup, "Agregar al carrito",
                        "/Agregar_Plato_Carrito")  # markup,
    logic.pintarBotones(markup, "Finalizar pedido",
                        "/comprar_productos")  # use
    logic.pintarBotones(markup, "Listar platos comprados 20",
                        "/Listar_Ultimos_Pedidos")  # user
    logic.pintarBotones(markup, "Editar estado pedido",
                        "/edita_estado_pedido")  # Admin
    bot.send_message(call.message.chat.id,
                     "Elije la opción que deseas ver:", reply_markup=markup)


@bot.callback_query_handler(func=lambda q: q.data == '/Listar_Ultimos_Pedidos')
def callback_query_ListarUltimosPedidos(call):
    response = bot.send_message(call.message.chat.id,
                                "Ingrese la cedula para consultar los pedidos")
    bot.register_next_step_handler(response, ListarPedidosXCedula)

    # bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda q: q.data == '/Agregar_Plato_Carrito')
def callback_query_AgregarPlatoCarrito(call):
    logic.ValidatefieldinDict(bot_data, call.message.chat.id)
    logic.ValidatefieldinDict(bot_data[call.message.chat.id], 'Pedido')
    logic.ValidatefieldinDict(
        bot_data[call.message.chat.id]['Pedido'], 'Productos', [])
    markup = logic.pintarCategoriasPedido()
    response = bot.send_message(
        call.message.chat.id, "¿Elija la categoria del producto?", reply_markup=markup)
    bot.register_next_step_handler(response, pedidoCat)


@bot.callback_query_handler(func=lambda q: q.data == '/comprar_productos')
def callback_query_Comprar_pedido(call):
    logic.ValidatefieldinDict(bot_data, call.message.chat.id)
    logic.ValidatefieldinDict(bot_data[call.message.chat.id], 'Pedido')
    logic.ValidatefieldinDict(
        bot_data[call.message.chat.id]['Pedido'], 'Productos', [])
    if len(bot_data[call.message.chat.id]['Pedido']['Productos']) > 0:
        text = logic.listarPedidoTemp(
            bot_data[call.message.chat.id]['Pedido']['Productos'])

        bot.send_message(call.message.chat.id, text)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("Continuar Comprando", callback_data="/Agregar_Plato_Carrito"),
                   types.InlineKeyboardButton("Finalizar y Pagar", callback_data="/Finalizar_Pedido"))
        bot.send_message(call.message.chat.id,
                         "Elije la opción con la que deseas continuar:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id,
                         "No has agregado ningun plato")


@bot.callback_query_handler(func=lambda q: q.data == '/Finalizar_Pedido')
def callback_query_cantidad_plato(call):
    logic.ValidatefieldinDict(bot_data, call.message.chat.id)
    logic.ValidatefieldinDict(bot_data[call.message.chat.id], 'Pedido')
    logic.ValidatefieldinDict(
        bot_data[call.message.chat.id]['Pedido'], 'Productos', [])
    if len(bot_data[call.message.chat.id]['Pedido']['Productos']) > 0:
        response = bot.send_message(
            call.message.chat.id, "¿Cual es su cedula?")
        bot.register_next_step_handler(response, pedidofinalizacionCedula)
    else:
        bot.send_message(call.message.chat.id,
                         "Aun no has agregado productos al carrito")


# -------------- Fin pedidos


""" Metodos-------------------------------------------------------------------------"""

# ------------Inicio Pedidos

def indicarIdPedido(message):
    try:
        logic.ValidatefieldinDict(bot_data,message.chat.id)
        logic.ValidatefieldinDict(bot_data[message.chat.id], 'pedido')
        bot_data[message.chat.id]['pedido']['id'] = message.text
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Pendiente', 'En proceso', 'Entregado', 'Cancelado')

        response = bot.send_message(message.chat.id,"Elije el tipo de estado", reply_markup=markup)
        bot.register_next_step_handler(response, indicarTipoDeEstado)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió en la edicion de los productos: {e}")
  
def indicarTipoDeEstado(message):
    try:
        if logic.actulizarEstadoPedido(bot_data[message.chat.id]['pedido']['id'],message.text):
            bot.send_message(message.chat.id, "Se ha Actualizado el pedido correctamente")
        else:
            bot.send_message(message.chat.id, "Valida de nuevo el tipo de Producto")
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió donde pensamos actualizar pedido: {e}")


def ListarPedidosXCedula(message):
    pedidos = logic.PedidosXCedula(message.text)
    text = logic.listarPedidos(pedidos)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def pedidoCat(message):
    try:
        productos = logic.ProductosXIdCat(message.text.split('-')[0])
        if len(productos) > 0:
            markup = logic.pintarBtnProductos(productos)
            response = bot.send_message(message.chat.id,
                                        "¿que producto de la categoria desea?:", reply_markup=markup)
            bot.register_next_step_handler(response, pedidoProducto)
        else:
            response = bot.send_message(
                message.chat.id, "Esta categoria aun no tiene productos")
            bot.register_next_step_handler(response, pedidoCat)
    except Exception as e:
        response = bot.reply_to(
            message, f"El valor ingresado no es correcto intenta nuevamente: {e}")
        bot.register_next_step_handler(response, pedidoCat)


def pedidoProducto(message):
    try:
        bot_data[message.chat.id]['Pedido']['UltimoProd'] = message.text.split(
            '-')[0]
        response = bot.reply_to(
            message, 'Indique la cantidad del producto que desea', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(response, pedidoCantidadProducto)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió 1: {e}")


def pedidoCantidadProducto(message):
    try:
        notexist = True
        for data in bot_data[message.chat.id]['Pedido']['Productos']:
            if data["idProd"] == bot_data[message.chat.id]['Pedido']['UltimoProd']:
                notexist = False
                data["Cantidad"] += int(message.text)
        if notexist:
            bot_data[message.chat.id]['Pedido']['Productos'].append(
                {
                    "idProd": bot_data[message.chat.id]['Pedido']['UltimoProd'],
                    "Cantidad": int(message.text)
                })
        bot.send_message(
            message.chat.id, 'Su producto se ha añadido correctamente', reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        response = bot.reply_to(
            message, f"pusiste un valor incorrecto, intenta nuevamente")
        bot.register_next_step_handler(response, pedidoCantidadProducto)


def pedidofinalizacionCedula(message):
    try:
        logic.ValidatefieldinDict(
            bot_data[message.chat.id]['Pedido'], 'Persona')
        bot_data[message.chat.id]['Pedido']['Persona']['Cedula'] = message.text
        bot_data[message.chat.id]['Pedido']['Cedula'] = message.text
        persona = logic.listaUsuarioXCedula(
            bot_data[message.chat.id]['Pedido']['Cedula'])
        if len(persona) > 0:
            print("Existe")
            # validar direccion y despues a pagar
            bot_data[message.chat.id]['Pedido']['Direccion'] = persona[0].direccion
            bot_data[message.chat.id]['Pedido']['IdPersona'] = persona[0].id
            markup = types.ReplyKeyboardMarkup(
                one_time_keyboard=True, input_field_placeholder="Confirma tu direccion")
            markup.add("Confirmar", "Cambiar")
            response = bot.send_message(message.chat.id,
                                        f"Confirma si quieres usar esta direccion: {persona[0].direccion}", reply_markup=markup)
            bot.register_next_step_handler(
                response, confirmacionDireccionPedido)
        else:
            CrearPersona(message)
            print("no Existe")
        # response = bot.reply_to(message, '¿Indique la Direccion del pedido?')
        # bot.register_next_step_handler(response, pedidofinalizacionDireccion)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió 0: {e}")


def pedidofinalizacionDireccion(message):
    try:
        bot_data[message.chat.id]['Pedido']['Direccion'] = message.text
        pagarProductos(message)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def pagarProductos(message):
    bot.send_message(message.chat.id, logic.guardarPago(
        bot_data[message.chat.id]['Pedido']), reply_markup=types.ReplyKeyboardRemove())


def confirmacionDireccionPedido(message):
    try:
        if message.text == 'Confirmar':
            pagarProductos(message)
        elif message.text == 'Cambiar':
            response = bot.send_message(message.chat.id,
                                        "Escribe la direccion que deseas usar", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(
                response, cambioDireccionPedido)
        else:
            bot.send_message(message.chat.id,
                             "No has seleccionado una opción valida")
            Editarcategoria(message, bot_data[message.chat.id]['idcateditar'])
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió donde pensamos: {e}")


def cambioDireccionPedido(message):
    bot_data[message.chat.id]['Pedido']['Direccion'] = message.text
    pagarProductos(message)

# -----------------Fin pedidos
# ------------------ Inicio Persona


def CrearPersona(message):
    response = bot.reply_to(
        message, '¿Cual es su nombre completo?', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(response, nombrePersona)


def nombrePersona(message):
    bot_data[message.chat.id]['Pedido']['Persona']['Nombre'] = message.text
    response = bot.reply_to(
        message, '¿Cual es su direccion para los envios?')
    bot.register_next_step_handler(response, direccionPersona)


def direccionPersona(message):
    bot_data[message.chat.id]['Pedido']['Persona']['Direccion'] = message.text
    response = bot.reply_to(
        message, '¿Cual es su telefono de contacto?')
    bot.register_next_step_handler(response, guardarPersona)


def guardarPersona(message):
    bot_data[message.chat.id]['Pedido']['Persona']['Telefono'] = message.text
    if logic.GuardarPesona(bot_data[message.chat.id]['Pedido']['Persona']):
        pedidofinalizacionCedula(message)
    else:
        bot.send_message(
            message.chat.id, 'No pudimos guardar tus datos')


"""--------------------------------------------------------------------------------------------------"""

# ---------------Inicio Productos


def NombrePlato(message):
    try:
        bot_data[message.chat.id] = {}
        bot_data[message.chat.id]['itemcategoria'] = {}
        bot_data[message.chat.id]['itemcategoria']['nombre'] = message.text
        response = bot.reply_to(message, '¿Indique descripción del plato')
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
        GuardarPlato(message)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def GuardarPlato(message):
    if logic.GuardarPlato(bot_data[message.chat.id]['itemcategoria']):
        bot.send_message(
            message.chat.id, "Se ha guardado el plato correctamente correctamente")

# TODO completar funcionalidad del editar
# def EditarPlato(message, id=None):
#     try:
#         if id == None:
#             id = message.text
#         ItemCategoria = logic.listar_Categorias_itemCategorias(id)
#         text = logic.getMessageCategoriasItems(ItemCategoria)
#         bot.reply_to(message, text, parse_mode="Markdown")

#         markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#         markup.add('Nombre', 'Descripcion', 'Estado', 'Precio', 'Categoria')

#         response = bot.send_message(message.chat.id,
#                                     "Elije el campo que deseas editar", reply_markup=markup)
#         bot_data[message.chat.id] = {}
#         bot_data[message.chat.id]['idProdEditar'] = id

#         bot.register_next_step_handler(
#             response, EditarcategoriaXtipo)

#     except Exception as e:

        bot.reply_to(message, f"Algo terrible sucedió: {e}")

# --------------Inicio Categorias


def Editarcategoria(message, id=None):
    try:
        if id == None:
            id = message.text
        Categorias = logic.listar_CategoriaXid(id)
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
        if message.text == 'Descripción':
            response = bot.send_message(message.chat.id,
                                        "Escribe el nuevo valor de la descripción", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(
                response, EditarcategoriaDescripcion)
        elif message.text == 'Estado':
            if logic.EditarCategoria(bot_data[message.chat.id]['idcateditar'], message.text, message.text):
                bot.send_message(message.chat.id,
                                 "Se ha editado el estado correctamente", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id,
                             "No has seleccionado una opción valida")
            Editarcategoria(message, bot_data[message.chat.id]['idcateditar'])
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió donde pensamos: {e}")


def EditarcategoriaDescripcion(message):
    if logic.EditarCategoria(bot_data[message.chat.id]['idcateditar'], "Descripción", message.text):
        bot.send_message(message.chat.id,
                         "Se ha editado la descripción correctamente")

# -------------- Fin Categorias
# ------------Manejo por defecto Handler


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
