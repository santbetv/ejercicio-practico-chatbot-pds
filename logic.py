import database.db as db
from telebot import types
from sqlalchemy.sql.expression import func, desc
from sqlalchemy import update
from models.Menu import Menu
from models.Categoria import Categoria
from models.ItemCategoria import ItemCategoria
from models.Persona import Persona
from models.Pedido import Pedido
from models.Rol import Rol
from models.ItemsCategoriaPedido import ItemsCategoriaPedido
import database.sql_restaurante as crearLimpiar


def Createmenu():
    # account = db.session.query(Menu).get(user_id)
    # db.session.commit()
    # if account == None:
    menu = Menu("1", "descripcion", "Estadotest")
    db.session.add(menu)
    db.session.commit()

    return True


def get_welcome_message(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* \n"
        "¡Estoy aquí para ayudarte!"      
    )
    return response
def get_welcome_messageAdmin(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* \n"
        "¡Estoy aquí para ayudarte, podrás: \n"
        "- Gestionar(adicionar, listar y Cambiar estado) los platos del restaurante.!\n"
        "- Gestionar los pedidos del restaurante"
    )
    return response


def get_welcome_messageUser(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* "
        "¡Estoy aquí para ayudarte con tus pedidos y compras, podrás: \n"
        "- Consultar los platos del restaurante \n"
        "- Gestionar tu carrito de compras\n"
        "- Revisar tu historial de compras de los últimos 20 platos."
    )
    return response


def get_fallback_message(text):
    response = f"\U0001F648 No entendí lo que me acabas de decir"
    return response


def on_subMenu(message, types):
    response = (
        "Selecciona una opción del menú:"
    )
    return response


def check_admin(user_id):
    admins = [1441882294]
    return user_id in admins
    # return False


def listar_Categorias():
    Categorias = db.session.query(Categoria).all()
    return Categorias


def listar_Categorias_itemCategorias():
    items = db.session.query(
        Categoria, ItemCategoria).join(ItemCategoria).all()
    # for c, i in items:
    #     print("plato: {} categoria: {} precio: {} estado: {} ".format(
    #         i.nombre, c.descripcion, i.precio, "Activo" if i.estado else "Inactivo"))
    return items


def listar_Categorias_itemCategorias_ByID(id):
    items = db.session.query(
        ItemCategoria, Categoria).join(ItemCategoria).filter_by(id=id).all()
    # for c, i in items:
    #     print("plato: {} categoria: {} precio: {} estado: {} ".format(
    #         i.nombre, c.descripcion, i.precio, "Activo" if i.estado else "Inactivo"))
    return items


def getMessageCategorias(Categorias):
    if len(Categorias) > 0:
        text = "``` Listado de Categorias:\n\n"
        text += '| ID | Descripcion | Estado\n'
        for Categoria in Categorias:
            text += f'| {Categoria.id} | {Categoria.descripcion} | {"Activo" if Categoria.estado else "Inactivo"} \n'
        text += "```"
    else:
        text = "No hay categorias por listar"
    return text


def getMessageCategoriasItems(items):
    text = "``` Listado de platos:\n\n"
    text += '| ID | Nombre | Precio | Estado |\n'
    for Categoria, item in items:
        text += f'| {item.id} | {item.nombre} | {item.precio} | {"Activo"  if item.estado else "Inactivo"} \n'
    text += "```"
    return text


def listarPedidoTemp(pedido):
    if len(pedido) > 0:
        text = "``` Listado del pedido:\n\n"
        text += '| ID | Nombre | Precio | Cant \n'
        total = 0
        for item in pedido:
            prod = listar_Categorias_itemCategorias_ByID(item["idProd"])[0][0]
            text += f'| {prod.id} | {prod.nombre} | {prod.precio} | {item["Cantidad"]} \n'
            total += (prod.precio*item["Cantidad"])
            # text += f'| {} | {item.nombre} | {item.precio} | {"Activo"  if item.estado else "Inactivo"} \n'

        text += f"Total: ${total}```"
    else:
        text = 'Aun no tiene datos en el pedido'
    return text


def listar_Categorias_X_Estado(estado):
    Categorias = db.session.query(Categoria).filter_by(estado=estado).all()
    return Categorias


def listaUsuarioXCedula(cedula):
    persona = db.session.query(Persona).filter_by(cedula=cedula).all()
    return persona


def GuardarPesona(personaCrear):
    try:
        persona = Persona(personaCrear["Cedula"], personaCrear["Nombre"],
                          personaCrear["Direccion"], personaCrear["Telefono"])
        db.session.add(persona)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def Guardarcategoria(descripcion):
    categoria = Categoria(descripcion, 1)
    db.session.add(categoria)
    db.session.commit()
    return True


def GuardarPlato(item):
    print(item)
    itemCategoria = ItemCategoria(
        item['nombre'], item['descripcion'], item['precio'], item['IdCategoria'])
    db.session.add(itemCategoria)
    db.session.commit()
    return True


""" tipos de estados Pendiente, En proceso, Entregado o Cancelado"""


def guardarPago(pedido):
    try:
        valortotal = 0
        for item in pedido["Productos"]:
            itemPrecio = db.session.query(Categoria, ItemCategoria).join(
                ItemCategoria).filter(ItemCategoria.id == item['idProd']).all()
            for c, i in itemPrecio:
                valortotal += i.precio * item['Cantidad']
        pedidoNuevo = Pedido(
            pedido['Direccion'], "Pendiente", valortotal, pedido['IdPersona'])
        db.session.add(pedidoNuevo)
        db.session.commit()
        for item in pedido["Productos"]:
            var = ItemsCategoriaPedido(pedidoNuevo.id, item['idProd'])
            db.session.add(var)
            db.session.commit()
        return "Se pago correctamente"
    except Exception as e:
        return f"Ocurrio un error: {e}"


def EditarCategoria(idcategoria, campo, valor):
    categoria = db.session.query(Categoria).get(idcategoria)
    db.session.commit()
    if not categoria:
        return False
    if campo == "Descripcion":
        categoria.descripcion = valor
    elif campo == "Estado":
        categoria.estado = False if categoria.estado else True
    db.session.commit()
    return True


def pintarCategoriasPedido():
    Categorias = db.session.query(Categoria).filter(
       not Categoria.estado == False).all()
    print(Categorias)
    markup = types.ReplyKeyboardMarkup(
        row_width=1, input_field_placeholder="Elija la Categoria del producto")
    for c in Categorias:
        markup.add(f"{c.id}- {c.descripcion}")
    return markup


def ProductosXIdCat(id):
    items = db.session.query(Categoria, ItemCategoria).join(
        ItemCategoria).filter(Categoria.id == id and ItemCategoria.estado == True).all()
    return items


def pintarBtnProductos(items):
    markup = types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Elija el producto que desea Adicionar")
    markup.row_width = 1
    for c, i in items:
        markup.add(f"{i.id} - {i.nombre} - ${i.precio}")
    return markup


def pintarBotones(markup, nombreBoton, ruta):
    markup.add(types.InlineKeyboardButton(nombreBoton, callback_data=ruta))
    return markup


def listar_CategoriaXid(id):
    Categorias = db.session.query(Categoria).filter(Categoria.id == id).all()
    return Categorias


def listar_PlatosXid(id):
    Itemcategoria = db.session.query(ItemCategoria).filter_by(id=id).all()
    return Itemcategoria


def ValidatefieldinDict(dict, field, initValue={}):
    try:
        dict[field]        
    except:
        dict[field] = initValue


def PedidosXCedula(cedula):
    pedidos = db.session.query(Pedido).filter(
        Persona.cedula == cedula).filter(ItemsCategoriaPedido.idPedido == Pedido.id).filter(Pedido.IdPersona == Persona.id).limit(20).all()
    # Persona.cedula == cedula).filter(ItemsCategoriaPedido.idPedido == Pedido.id).filter(Pedido.IdPersona == Persona.id).order_by(desc(Pedido.fechaCreacion)).all()    
    for pedido in pedidos:
        print(
            f"id {pedido.id} | estado {pedido.estado} - valor {pedido.valorTotal}- fecha:{pedido.fechaCreacion}")
    return pedidos


def listarPedidos(pedidos):
    if len(pedidos) > 0:
        text = "``` Listado de Pedidos:\n\n"
        text += '| ID | Estado | Valor | Fecha\n'
        for pedido in pedidos:
            text += f'| {pedido.id} | {pedido.estado} | {pedido.valorTotal} | {pedido.fechaCreacion}\n'
        text += "```"
    else:
        text = "No hay pedidos asociados a este numero de cedula"
    return text

def actulizarEstadoPedido(item,estado):
    valor =db.session.query(Pedido).filter(Pedido.id == item).update({Pedido.estado:estado}, synchronize_session='evaluate')
    if valor==0:
        return False
    db.session.commit()
    return True

def listarPorEstadoPedido(estado):
    items = db.session.query(Pedido).filter(Pedido.estado == estado).all()
    return items