import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "restaurante.sqlite")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# cursor.execute('DELETE FROM tbl_Menus;');
# cursor.execute('DELETE FROM tbl_Categorias;');
# cursor.execute('DELETE FROM tbl_ItemsCategoria;');
# cursor.execute('DELETE FROM tbl_Pedidos;');
# cursor.execute('DELETE FROM tbl_ItemsCategoriaPedidos;');

# cursor.execute("INSERT INTO tbl_Roles(idRol,NombreRol) VALUES (1,'Prueba')");
# cursor.execute("INSERT INTO  tbl_Roles ( idRol , NombreRol ) VALUES (2,'Usuario')");

# cursor.execute("INSERT INTO  tbl_Personas ( idPersona , nombrePersona , apellidoPersona , direccionPersona , telefonoPersona , barrioPersona , idRol ) VALUES (1,'Santiago','Betancur','calle 16 # 15 14','America','3146593910','1')");
# cursor.execute("INSERT INTO  tbl_Personas ( idPersona , nombrePersona , apellidoPersona , direccionPersona , telefonoPersona , barrioPersona , idRol ) VALUES (2,'Sebastian','Gomez','calle 32 56 # 96','santander','3113710249','2')");

# cursor.execute("INSERT INTO tbl_Menus(descripcionMenu, estadoMenu) VALUES ('Menu Almuerzo','A')");
# cursor.execute("INSERT INTO tbl_Categorias(idCategoria,descripcionCategoria, estadoCategoria, idMenuCategoria) VALUES (1,'Pasta','A', 1)");
# cursor.execute("INSERT INTO tbl_Categorias(idCategoria,descripcionCategoria, estadoCategoria, idMenuCategoria) VALUES (2,'Pescado','A', 1)");
# cursor.execute("INSERT INTO tbl_Categorias(idCategoria,descripcionCategoria, estadoCategoria, idMenuCategoria) VALUES (3,'Jugo','A', 1)");

# cursor.execute("INSERT INTO tbl_ItemsCategoria(idItemCategoria,nombreItemCategoria,descripcionItemCategoria, estadoItemCategoria, precioItemCategoria, descuentoItemCategoria, idCategoria) VALUES (1,'Pasta napolina','Con salsa de tomates fresco',5000,0,'A', 1)");
# cursor.execute("INSERT INTO tbl_ItemsCategoria(idItemCategoria,nombreItemCategoria,descripcionItemCategoria, estadoItemCategoria, precioItemCategoria, descuentoItemCategoria, idCategoria) VALUES (2,'Pasta italiana','Con champiñones de peru, y pollo de japon',5000,0,'A', 1)");

# cursor.execute("INSERT INTO tbl_ItemsCategoria(idItemCategoria,nombreItemCategoria,descripcionItemCategoria, estadoItemCategoria, precioItemCategoria, descuentoItemCategoria, idCategoria) VALUES (3,'Mora en Leche','',5000,0,'A', 3)");
# cursor.execute("INSERT INTO tbl_ItemsCategoria(idItemCategoria,nombreItemCategoria,descripcionItemCategoria, estadoItemCategoria, precioItemCategoria, descuentoItemCategoria, idCategoria) VALUES (4,'Mango en Leche','',5000,0,'A', 3)");
# cursor.execute("INSERT INTO tbl_ItemsCategoria(idItemCategoria,nombreItemCategoria,descripcionItemCategoria, estadoItemCategoria, precioItemCategoria, descuentoItemCategoria, idCategoria) VALUES (5,'Mango en Agua','',5000,0,'A', 3)");

# cursor.execute("INSERT INTO tbl_Pedidos(idPedido, direccionPedido, estadoPedido,valorTotalPedido, idPersona) VALUES (1,'Calle 30 25 # 56','A',45000, 1)");

# cursor.execute("INSERT INTO tbl_ItemsCategoriaPedidos(idItemCategoriaPedido, idPedido, idItemCategoria) VALUES (1,1,1)");


conn.commit()
cursor.close()
conn.close()