
from flask import Flask, request, jsonify
from flask import request

from flask_cors import CORS

import mysql.connector

from werkzeug.utils import secure_filename

import os
import time

#--------------------------------------------------------------------


app = Flask(__name__)
CORS(app) 


#============================ Clase Principal =======================

class Catalogo:
    
    def __init__(self, host, user, password, database):
       
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        
        
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err


# ====================== Tabla Productos ================================       
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            id INT,
            titulo VARCHAR(255) NOT NULL,
            categoria_nombre VARCHAR(255) NOT NULL,
            precio INT NOT NULL,
            imagen_url VARCHAR(255),
            categoria_id VARCHAR(255) NOT NULL )''')
        self.conn.commit()



        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
        
#==================== Tabla Carrito ==============================
 

        self.crear_tabla_carrito()

    def crear_tabla_carrito(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS carrito (
            id INT,
            titulo VARCHAR(255) NOT NULL,
            categoria_nombre VARCHAR(255) NOT NULL,
            precio INT NOT NULL,
            imagen_url VARCHAR(255),
            categoria_id VARCHAR(255) NOT NULL )''')
        self.conn.commit()
        
        
        
        
        
#======================================= FUNCIONES ========================================       
        
        
#============ Función para cargar inicialmente todos los productos de la tienda (GET) ==================
    
    def listar_productos(self):
       #Consulta SQL para obtener todos los registros de la tabla 'productos'
        self.cursor.execute("SELECT * FROM productos")
        
        # Obtención de los resultados de la consulta (método .fetchall())
        productos = self.cursor.fetchall()
        # Retorno de la lista de productos obtenida de la base de datos
        return productos
            
            
    ##=================== Función para agregar un registro a la tabla (POST) ========================
    
                                                                    ###########
    def agregar_producto(self, id, titulo, categoria_nombre, precio, imagen_url, categoria_id):

        #Realizamos la consulta SQL
        self.cursor.execute(f"SELECT * FROM productos WHERE id = {id}")
        # Aloja el retorno de la consulta del producto deseado (método .fetchone())
        producto_existe = self.cursor.fetchone()
        
        if producto_existe:
            return False
        
        #Variable que aloja la consulta SQL para insertar valores           
        sql = "INSERT INTO productos (id, titulo, categoria_nombre, precio, imagen_url, categoria_id) VALUES (%s, %s, %s, %s, %s, %s)"
        #Variable para solicitar cambios                      
        valores = (id, titulo, categoria_nombre, precio, imagen_url, categoria_id)
        #Realiza la consulta SQL y pide valores
        self.cursor.execute(sql,valores)
        #Confirma los cambios
        self.conn.commit()
        return True     
             
        
  #========= Función para cargar todos productos existentes en el carrito (GET) =================
    
    def carrito_productos(self):
       #Consulta SQL para obtener todos los registros de la tabla 'carrito'
        self.cursor.execute("SELECT * FROM carrito")
        
        # Obtención de los resultados de la consulta (método .fetchall())
        carrito = self.cursor.fetchall()
        # Retorno de la lista de productos obtenida de la base de datos
        return carrito
      
        
        
 #================ Función del botón que agrega al carrito (GET) ===============
    
    def boton_agregar(self, id):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE id = {id}")
        # Retorna la consulta del producto deseado (método .fetchone())
        return self.cursor.fetchone()    

        
        
#========= Función que agrega los productos seleccionados por el botón al carrito (POST) ==============================


    def agregar_al_carrito(self, id):
        
        producto = self.boton_agregar(id)

        if producto:
            
            self.cursor.execute('''INSERT INTO carrito (id, titulo, categoria_nombre, precio, imagen_url, categoria_id)
                                   VALUES (%s, %s, %s, %s, %s, %s)''',
                                (producto['id'], producto['titulo'], producto['categoria_nombre'],
                                 producto['precio'], producto['imagen_url'], producto['categoria_id']))
            self.conn.commit()
            return True
        else:
            
            return False



    #================ Función para filtrar una categoria (GET) ===============
    
    def filtrar_categoria(self, categoria_id):
    
        self.cursor.execute("SELECT * FROM productos WHERE categoria_id = %s", (categoria_id,))
        # Obtención de los resultados de la consulta (método .fetchall())
        productos = self.cursor.fetchall()
        # Retorno de la lista de productos obtenida de la base de datos
        return productos
    
    

    #=============== Función para eliminar un producto del carrito (DELETE) =========================
    
    def eliminar_producto(self, id):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM carrito WHERE id = {id}")
        #confirmamos los cambios
        self.conn.commit()
        #verifica si al menos una fila fué afectada (al ser mayor que 0 se eliminó una fila)
        return self.cursor.rowcount > 0



#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------

#CONEXIÓN A LA BASE DE DATOS

catalogo = Catalogo(host='localhost', user='root', password='root', database='tienda_funkopop')


#=============================================================================================
# Carpeta para guardar las imagenes
ruta_destino = 'static/img'


#======================= Agregamos productos iniciales a la tabla (POST) ====================

catalogo.agregar_producto(1, 'Pop! Rey', 'Star Wars', 19990, '1.png', 'starwars')
catalogo.agregar_producto(2, 'Pop! Cobb Vanth', 'Star Wars', 18990, '2.png', 'starwars')
catalogo.agregar_producto(3, 'Pop! Luke Skywalker', 'Star Wars', 21990, '3.png', 'starwars')
catalogo.agregar_producto(4, 'Pop! Darth Maul', 'Star Wars', 22990, '4.png', 'starwars')
catalogo.agregar_producto(5, 'Pop! Dark Trooper', 'Star Wars', 17990, '5.png', 'starwars')
catalogo.agregar_producto(6, 'Pop! Han Solo', 'Star Wars', 23990, '6.png', 'starwars')
catalogo.agregar_producto(7, 'Pop! Anakyn', 'Star Wars', 22990, '7.png', 'starwars')

catalogo.agregar_producto(8, 'Pop! Scorbunny', 'Pokemon', 14990, '8.png', 'pokemon')
catalogo.agregar_producto(9, 'Pop! Arcanine', 'Pokemon', 14990, '9.png', 'pokemon')
catalogo.agregar_producto(10, 'Pop! Charizard', 'Pokemon', 22990, '10.png', 'pokemon')
catalogo.agregar_producto(11, 'Pop! Psyduck', 'Pokemon', 14990, '11.png', 'pokemon')
catalogo.agregar_producto(12, 'Pop! Evee', 'Pokemon', 15990, '12.png', 'pokemon')
catalogo.agregar_producto(13, 'Pop! Alakazam', 'Pokemon', 15990, '13.png', 'pokemon')

catalogo.agregar_producto(14, 'Pop! Party Thor', 'Marvel', 19990, '20.png', 'marvel')
catalogo.agregar_producto(15, 'Pop! Zombie Iron Man', 'Marvel', 18990, '21.png', 'marvel')
catalogo.agregar_producto(16, 'Pop! Thanos', 'Marvel', 24990, '22.png', 'marvel')
catalogo.agregar_producto(17, 'Pop! Iron Man', 'Marvel', 31990, '23.png', 'marvel')
catalogo.agregar_producto(18, 'Pop! Hulk', 'Marvel', 18990, '24.png', 'marvel')
catalogo.agregar_producto(19, 'Pop! Thor', 'Marvel', 17990, '25.png', 'marvel')

catalogo.agregar_producto(20, 'Pop! Raya', 'Disney', 15990, '14.png', 'disney')
catalogo.agregar_producto(21, 'Pop! Zero', 'Disney', 13990, '15.png', 'disney')
catalogo.agregar_producto(22, 'Pop! Eve', 'Disney', 18990, '16.png', 'disney')
catalogo.agregar_producto(23, 'Pop! Stitch', 'Disney', 17990, '17.png', 'disney')
catalogo.agregar_producto(24, 'Pop! Merida', 'Disney', 15990, '18.png', 'disney')
catalogo.agregar_producto(25, 'Pop! Goofy', 'Disney', 17990, '19.png', 'disney')



#====================================== ENDPOINTS ============================================
 
#------ Endpoint para cargar inicialmento todos los productos de la tienda (GET)*  ----------------------------------------

@app.route("/productos", methods=["GET"])
def listar_productos():
    #llama a la función
    productos = catalogo.listar_productos()
    #devuelve el JSON
    return jsonify(productos)




#------- Endpoint para cargar todos productos existentes en el carrito (GET) * ----------------------------------------

@app.route("/carrito", methods=["GET"])
def carrito_productos():
    #llama a la función
    carrito = catalogo.carrito_productos()
    #devuelve el JSON
    return jsonify(carrito)


#--------------------------Endpoint para insertar productos en el carrito *---------------------

@app.route("/carrito/<int:id>", methods=["POST"])
def agregar_al_carrito(id):
    # Llama a la función que agrega el producto al carrito
    insertar = catalogo.agregar_al_carrito(id)
    
    if insertar:
        return jsonify({"mensaje": "Producto agregado al carrito exitosamente"})
    else:
        return jsonify({"mensaje": "Error al agregar el producto al carrito"}), 500




#------------------------------  Endpoint para filtrar categoría ----------------------------------------

@app.route("/productos/<categoria_id>", methods=["GET"])
def filtrar_categoria(categoria_id):
    # llama a la función pasando el parámetro categoria_id
    productos = catalogo.filtrar_categoria(categoria_id)
    # devuelve el JSON
    return jsonify(productos)



#----------------------Endpoint para eliminar un producto del carrito *---------------------

@app.route("/carrito/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    # Llama a la función que elimina el producto del carrito
    eliminar = catalogo.eliminar_producto(id)
    
    if eliminar:
        return jsonify({"mensaje": "Producto eliminado exitosamente"})
    else:
        return jsonify({"mensaje": "Error al eliminar el producto del carrito"}), 500


if __name__ == "__main__":
    app.run(debug=True)
