from psycopg2 import connect, Error
from tkinter import Tk, Canvas, Label, Frame, Entry, Button, W, E, Listbox, END

def connection():
    try:
        connection = connect(
            host='localhost',
            database='taller_3',
            user='postgres',
            password='pingui840', 
            port='5432')
        return connection
    except(Exception, Error) as error:
        connection.rollback()
        print("Error: %s" % error)


def insert_query(query,data):
    try:
        con = connection()
        if con and query != '' and data != []: #Con mas parametros (WHERE - INSERT)
            cursor = con.cursor()
            cursor.execute(query,data)
        con.commit()
    except(Exception, Error) as error:
        print("Error: %s" % error)

        

def select_query(query,data=[]):
    try:
        con = connection()
        cursor = con.cursor()
        if con and query != '' and data == []:
            cursor.execute(query)
        elif con and query != '' and data != []: #Con mas parametros 
            cursor.execute(query,data)
        result = cursor.fetchall()
        return result
    except(Exception, Error) as error:
        print("Error: %s" % error)

def update_query(query,data=[]):
    try:
        con = connection()
        cursor = con.cursor()
        if con and query != '' and data == []:
            cursor.execute(query)
        elif con and query != '' and data != []: #Con mas parametros 
            cursor.execute(query,data)
        con.commit()
    except(Exception, Error) as error:
        print("Error: %s" % error)


def delete_query(query,data=[]):
    try:
        con = connection()
        cursor = con.cursor()
        if con and query != '' and data == []:
            cursor.execute(query)
        elif con and query != '' and data != []: #Con mas parametros 
            cursor.execute(query,data)
        con.commit()
    except(Exception, Error) as error:
        print("Error: %s" % error)


def menu_cliente(rut):
    menu  = False
    print(".....Bienvenido/a al menu ....")
    print("1. Cambiar contraseña")
    print("2. Elegir un producto para añadir al carrito")
    print("3. Ver Saldo")
    print("4. Recargar Saldo")
    print("5. Ver Carrito")
    print("6. Quitar producto del carrito")
    print("7. Pagar Carrito")
    opcion = int(input("Ingrese la opcion que desea realizar: "))
    if(opcion <6):
        menu = True
    else:
        menu = False
    while menu :
        if (opcion == 1):#uwu
            print("se comenzará con el cambio de contraseña . . .")
            password = str(input("a continuacion se le pedira que ingrese su contraseña actual: "))
            query = "SELECT passw FROM cliente WHERE rut = %s AND passw = %s "
            login = select_query(query,[rut,password])
            while (login == []) :
                password = str(input("Error,Ingrese su contraseña nuevamente: "))
                query = "SELECT rut FROM cliente WHERE rut = %s AND passw = %s"
                login = select_query(query,[rut,password])

            new_password = str(input("Ingrese su nueva contraseña: "))
            verify_password = str(input("Ingrese nuevamente su nueva contraseña: "))
            while (new_password != verify_password):
                print("Error, las contraseñas no coinciden")
                new_password = str(input("Ingrese su nueva contraseña: "))
                verify_password = str(input("Ingrese nuevamente su nueva contraseña: "))

            query = "UPDATE cliente SET passw = %s WHERE rut = %s"
            update_query(query,[verify_password,rut])
            print("Contraseña actualizada con exito")
            print("------------------------------------------------")

        if(opcion == 2): #Elegir un producto para añadir al carrito
            print("se comenzará con la eleccion de un producto . . .")
            query = "SELECT * FROM producto"
            result = select_query(query)
            if result != []:
                for i in result:
                    print("producto: ",i[0]," precio: ",i[1]," stock: ",i[2])
            else:
                print("No hay productos disponibles por el momento")
            
            #elegir el producto
            id_producto = str(input("Ingrese el id del producto que desea añadir al carrito: "))
            query = "SELECT * FROM producto WHERE id_producto = %s"
            result = select_query(query,[id_producto])
            

            print("TESTEO : ",result[0][0])

            while (result == [] or result[0][0]== None):
                id_producto = str(input("Error, no se encontro el producto, ingrese nuevamente el id del producto: "))
                query = "SELECT * FROM producto WHERE id_producto = %s"

            #elegir cantidad
            cantidad = int(input("Ingrese la cantidad que desea comprar: "))
            stock = result[0][2]
            while (cantidad > stock):
                print("Error, no hay stock suficiente")
                cantidad = int(input("Ingrese la cantidad que desea comprar: "))

            #añadir al carrito
                
            query = "SELECT * FROM producto WHERE producto_id = %s"
            result = select_query(query,[rut])

            query = "SELECT * FROM carrito WHERE rut = %s"
            result = select_query(query,[rut])

            """FALTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""
            """FALTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""

        if(opcion == 3):
            print("Ingrese el rut del usuario que desea bloquear")
        if(opcion == 4):
            print("Ingrese el rut del usuario que desea bloquear")
        if(opcion == 5):
            print("Ingrese el rut del usuario que desea bloquear")
        if(opcion == 6):
            print("Gracias por utilizar el sistema...saliendo")

        continuar = str(input("Desea realizar otra accion? (si/no): "))
        if(continuar.lower() == "si"):
            menu_cliente(rut)
        else:
            print("Gracias por utilizar el sistema...saliendo")
            menu = False

def menu_Administrador():
    menu = False
    print(".....Bienvenido/a al menu administrador....")
    print("1. Bloquear usuario")
    print("2. Ver el historial de compras de algun cliente")
    print("3. Agregar producto")
    print("4. Agregar stock")
    print("5. Actualizar datos de un producto")
    print("6. salir")
    opcion = int(input("Ingrese la opcion que desea realizar: "))
    if(opcion <6):
        menu = True
    else:
        menu = False
    while menu:
        if (opcion == 1):# chekeado
            usuario = str(input("Ingrese el usuario que desea bloquear: "))
            query = "SELECT usuario FROM cliente WHERE usuario = %s"
            result = select_query(query,[usuario])
            
            while (result == []):
                usuario = str(input("Ingrese el usuario que desea bloquear: "))
                query = "SELECT usuario FROM cliente WHERE usuario = %s"
                result = select_query(query,[usuario])

            usuario = result[0][0]
            print(usuario)
            query = "SELECT carrito_id FROM cliente WHERE usuario =%s"
            carrito_id = select_query(query,[usuario])
            carrito_eliminar = carrito_id[0][0]
            print(carrito_eliminar)

            query = "DELETE FROM cliente WHERE usuario =%s"
            delete_query(query,[usuario])
            query = "DELETE FROM carrito WHERE carrito_id =%s"
            delete_query(query,[carrito_eliminar])

            print("Usuario ",usuario," ha sido bloqueado")
            print("------------------------------------------------")
            break

        if(opcion == 2):#checkeado
            query  = "SELECT * FROM cliente"
            result = select_query(query)
            if result != []:
                rut_usuario = str(input("Ingrese el rut del usuario que desea ver el historial de compras: "))
                query = "SELECT cliente.rut , cliente.usuario, venta.producto_id, venta.valor_total,venta.venta_id FROM historial_de_ventas INNER JOIN cliente on cliente.rut = historial_de_ventas.rut INNER JOIN venta ON venta.venta_id = historial_de_ventas.venta_id WHERE historial_de_ventas.rut = %s"
                result = select_query(query,[rut_usuario])
                while query == []: #si se equivoca en el ingreso del rut
                    print("Error, el rut ingresado no existe")
                    rut_usuario = str(input("Ingrese el rut del usuario que desea ver el historial de compras: "))
                    query = "SELECT cliente.rut , cliente.usuario, venta.producto_id, venta.valor_total,venta.venta_id FROM historial_de_ventas INNER JOIN cliente on cliente.rut = historial_de_ventas.rut INNER JOIN venta ON venta.venta_id = historial_de_ventas.venta_id WHERE historial_de_ventas.rut = %s"     
                    result = select_query(query,[rut_usuario])
                print("------------------Historial de compras-----------")
                print("Rut: ",rut[0][0])
                for i in result:
                    print("rut: ",i[0]," usuario: ",i[1]," producto_id: ",i[2]," valor_total: ",i[3]," venta_id: ",i[4])
                
            else:
                print("no hay clientes registrados aun :c")
            print("------------------------------------------------")

        if(opcion == 3):
            print("Ingrese el rut del usuario que desea bloquear")
        if(opcion == 4):
            print("Ingrese el rut del usuario que desea bloquear")
        if(opcion == 5):
            print("Ingrese el rut del usuario que desea bloquear")
        print("------------------------------------------------")
        continuar = str(input("Desea realizar otra accion? (si/no): "))
        if(continuar.lower() == "si"):
            menu_Administrador()
        else:
            print("Gracias por utilizar el sistema...saliendo")
            menu = False



print("============================================================")
print("=========Bienvenido/a al Negocio de Juanita :D==============")
print()

# creacion de login
try:
    rut = str(input("Ingrese su rut: "))
    if(rut.lower() != "admin"): # es un cliente
        query = "SELECT rut FROM cliente WHERE rut = %s"
        resultado = select_query(query,[rut])
        if (resultado != []): # el rut esta en la base de datos
            password = str(input("Ingrese su contraseña: "))
            query = "SELECT rut FROM cliente WHERE rut = %s AND passw = %s"
            login = select_query(query,[rut,password])
            while (login == []) :
                password = str(input("Error,Ingrese su contraseña nuevamente: "))
                query = "SELECT rut FROM cliente WHERE rut = %s AND passw = %s"
                login = select_query(query,[rut,password]) 
            menu_cliente(rut)

        else: # si el rut no se encuentra en la base de datos
            print("El rut ingresado no existe o esta erroneo...")
            registro = str(input("Esta registrarado? (si/no):"))
            if (registro.lower() == "si" ): #si se equivoco en el rut
                rut = str(input("Ingrese su rut nuevamente: "))
                query = "SELECT rut FROM cliente WHERE rut = %s "
                resultado = select_query(query,[rut])
                while resultado == []: # si se sigue equivocando
                    rut = str(input("Error,Ingrese su rut nuevamente: "))
                    query = "SELECT rut FROM cliente WHERE rut = %s AND passw = %s"
                    resultado = select_query(query,[rut])
                password = str(input("Ingrese su contraseña: "))
                query = "SELECT rut FROM cliente WHERE rut = %s AND passw = %s"
                login = select_query(query,[rut,password])
                while (login == []) :
                    password = str(input("Error,Ingrese su contraseña nuevamente: "))
                    query = "SELECT rut FROM cliente WHERE rut = %s AND passw = %s"
                    login = select_query(query,[rut,password]) 
                menu_cliente(rut)   

            else: # si no esta registrado
                query = "SELECT SUM(cant_carritos) FROM (SELECT COUNT(carrito_id) AS cant_carritos FROM carrito GROUP BY carrito_id) AS tabla"
                resultado = select_query(query)
                if resultado[0][0] == None:
                    cant_carritos = 0
                else:
                    cant_carritos = resultado[0][0]

                print("Ingrese sus datos para registrarse")
                usuario = str(input("Ingrese su nombre: "))
                carrito_id = cant_carritos + 1
                print("carrito_id:  ",str(carrito_id))
                query = "INSERT INTO carrito (carrito_id,monto_total) VALUES (%s,0) "
                insert_query(query,[carrito_id]) 
                password = str(input("Ingrese su contraseña: "))
                saldo = int(input("Ingrese su saldo: "))
                query = "INSERT INTO cliente (usuario,rut,carrito_id,passw,saldo) VALUES (%s,%s,%s,%s,%s)"
                insert_query(query,[usuario,rut,carrito_id,password,saldo])
                print("Se ha registrado correctamente")
    else:# es admin
        password = str(input("Ingrese su contraseña: "))
        while password.lower() != "negociojuanita": #se equivocó en la contraseña
            password = str(input("Error,Ingrese su contraseña nuevamente: "))
        menu_Administrador()

except Exception as error:
    print("Error: %s" % error)

finally:
    print("apagando . . .")
    connection().close()






 