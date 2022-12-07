import database.db as db
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
        "¡Estoy aquí para ayudarte, podrás: \n"
        "- Consultar los platos del restaurante \n"
        "- Gestionar tu carrito de compras\n"
        "- Revisar tu historial de compras de los últimos 20 platos."
    )
    return response

def get_fallback_message (text):
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

def listar_Categorias_X_Estado(estado):
    # Categorias = db.session.query(Categoria).all()
    Categorias = db.session.query(Categoria).filter_by(estado= estado)
    return Categorias

def listar_id(id):
    Categorias = db.session.query(Categoria).filter_by(id=id)
    return Categorias