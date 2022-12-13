import unittest2
import database.db as db
import logic
from models.Menu import Menu
from models.Categoria import Categoria
from models.ItemCategoria import ItemCategoria
from models.Persona import Persona
from models.Pedido import Pedido
from models.Rol import Rol
from models.ItemsCategoriaPedido import ItemsCategoriaPedido


class TestApp(unittest2.TestCase):
    
    def test_validar_total_del_producto(self):
        
        # Arrange
        precio=40000
        cantidad=4
        
        # Act
        proceso= logic.multiplicarPorCantidad(precio,cantidad)
        
        #Assert
        self.assertTrue(proceso == 160000)
        
    
    def test_validar_retorno_de_cesula_usuario_correcto(self):
        
        # Arrange
        persona=Persona(1053831993, 'Santiago Betancur', 'Calle 45 67 8', '3165106361', 2)
        cedulaPersona =persona.cedula
        # Act
        
        #Assert
        self.assertTrue(cedulaPersona == 1053831993)
    
    
if __name__ == '__main__':
    unittest2.main()
    
    
    