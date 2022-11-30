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


def check_admin(user_id):
    admins = [ 1441882294]
    return user_id in admins    
    # return False
