from psycopg2 import connect, Error
from tkinter import Tk, Canvas, Label, Frame, Entry, Button, W, E, Listbox, END

def connection():
    try:
        connection = connect(
            host='localhost',
            database='Taller_3',
            user='postgres',
            password='1685', 
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
    print("8. Salir")
    opcion = int(input("Ingrese la opcion que desea realizar: "))
    if(opcion <7):
        menu = True
    else:
        menu = False
    while menu:
        if (opcion == 1):#uwu
            print("se comenzará con el cambio de contraseña . . .")
            password = str(input("a continuacion se le pedira que ingrese su contraseña actual: "))
            query = "SELECT pass FROM cliente WHERE rut = %s AND pass = %s "
            login = select_query(query,[rut,password])
            while (login == []) :
                password = str(input("Error,Ingrese su contraseña nuevamente: "))
                query = "SELECT rut FROM cliente WHERE rut = %s AND pass = %s"
                login = select_query(query,[rut,password])

            new_password = str(input("Ingrese su nueva contraseña: "))
            verify_password = str(input("Ingrese nuevamente su nueva contraseña: "))
            while (new_password != verify_password):
                print("Error, las contraseñas no coinciden")
                new_password = str(input("Ingrese su nueva contraseña: "))
                verify_password = str(input("Ingrese nuevamente su nueva contraseña: "))

            query = "UPDATE cliente SET pass = %s WHERE rut = %s"
            update_query(query,[verify_password,rut])
            print("Contraseña actualizada con exito")
            

        if(opcion == 2): #Elegir un producto para añadir al carrito

            #obtengo el carrito de la persona
            query = "SELECT * FROM cliente WHERE rut = %s"
            result = select_query(query,[rut])
            carrito_id = result[0][2]


            print("seleccione algun producto:")
            print()
            query = "SELECT * FROM producto"
            result = select_query(query)
            if result != []:
                for i in result:
                    print("producto: ",i[0])
                    print(" precio: ",i[1])
                    print(" stock: ",i[2])
                    print("______________________________________________________________________")
            else:
                print("No hay productos disponibles por el momento")
            
            #elegir el producto
            producto_id = str(input("Ingrese el id del producto que desea añadir al carrito: "))
            query = "SELECT * FROM producto WHERE producto_id = %s"
            result = select_query(query,[producto_id])

            while (result == [] or result[0][0]== None):
                producto_id = str(input("Error, no se encontro el producto, ingrese nuevamente el id del producto: "))
                query = "SELECT * FROM producto WHERE producto_id = %s"

            #datos para el registro en el carrito
            precio = result[0][1]
            stock = result[0][2]

            #elegir cantidad
            cantidad_real = int(input("Ingrese la cantidad que desea comprar: "))
            while (cantidad_real > stock):
                print("Error, no hay stock suficiente")
                cantidad = int(input("Ingrese la cantidad que desea comprar: "))

            #añadir al carrito  
            query = "INSERT INTO carrito_productos (carrito_id,producto,cantidad_a_comprar,monto_total) VALUES (%s,%s,%s,%s)"
            insert_query(query,[carrito_id,producto_id,cantidad_real,precio*cantidad_real])
           
            #imprime el carrito
            query = "SELECT * FROM carrito_productos WHERE carrito_id = %s"
            result = select_query(query,[carrito_id])
            print("Carrito actual:")
            for i in result:
                print("producto: ",i[1],"| cantidad: ",i[2],"| monto total: ",i[3])

        if(opcion == 3):
            query = "SELECT saldo FROM cliente WHERE rut = %s"
            result = select_query(query,[rut])
            print("Su saldo actual es: $",result[0][0])

        if(opcion == 4):
             print("Recargar saldo")
             recarga = int(input("Inserte la cantidad que desea recargar:"))
             query = "UPDATE cliente SET saldo = cliente.saldo + %s WHERE cliente.rut = %s"
             update_query(query,[recarga,rut])
             break

        if(opcion == 5):
            print("Ver carrito")
            query = "SELECT producto_id,COUNT(*) from carrito_productos WHERE EXISTS(SELECT rut FROM cliente WHERE cliente.rut = %s) GROUP by carrito_productos.producto_id) "
            select_query(query,[rut])
            break
        if(opcion == 6):
            print("Quitar del carrito")
            id_eliminar = str(input("Ingrese el id del producto que desea eliminar del carrito"))
            cant_eliminar = int(input("Ingrese la cantidad del producto que desea eliminar:"))
            query ="DELETE FROM carrito_productos WHERE carrito_productos.producto_id = %s"
            delete_query(query,[id_eliminar])
            query2 = "UPDATE producto SET stock = producto.stock-%s WHERE producto.id_producto = %s"
            update_query(query2,[cant_eliminar,id_eliminar])
            break
        if(opcion == 7):
                print("Pagar carrito")
                query = "SELECT monto_acumulado FROM carrito WHERE EXISTS(SELECT * FROM cliente WHERE cliente.rut = %s )"#revisar q el monto no sea 
                select_query(query,[rut])
                respuesta = str(input("Desea pagar?:"))
                if(respuesta.lower() == "si"):
                    #verificar que lo pueda pagar
                    
                    query = "UPDATE cliente SET saldo = cliente.saldo - "
                    break

        continuar = str(input("Desea realizar otra accion? (si/no): "))
       
        print("-----------------------------------------------------------------------------------------")
        print("-----------------------------------------------------------------------------------------")
        if(continuar.lower() == "si"):
            menu_cliente(rut)
        elif(continuar.lower() == "no"):
            print("Gracias por utilizar el sistema...saliendo")
            menu = False
            opcion = 7

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

        if(opcion == 3):
            print("Agregar producto:")
            producto = str(input("Ingrese el nombre del producto que desea agregar:"))
            precio = str(input("Ingrese el precio del nuevo producto"))
            stock = int(input("Ingrese el stock del nuevo producto:"))
            query = "INSERT INTO producto(producto_id,precio,stock) VALUES (producto,precio,stock)"
            insert_query(query,[producto,precio,stock])

        if(opcion == 4):
            print("Agregar stock:")
            producto = str(input("Ingrese el nombre del producto:"))
            stock = int(input("Ingrese la cantidad de stock que desea agregar:"))
            query = "UPDATE producto SET stock = producto.stock + %s WHERE producto.id_producto = %s"
            update_query(query,[stock,producto])
    
        if(opcion == 5):
            print("Actualizar datos de un producto:")
            producto_ingresdo = str(input("Ingrese el nombre del producto que desea modificar:"))
            print("Modificaciones disponibles:")
            print("1.Precio")
            print("2.Nombre")
            print("3.Ambas")
            respuesta = int(input("Ingrese una opcion:"))
            if respuesta == 1:
                nuevo_precio = int(input("Ingrese el nuevo precio:"))
                query = "UPDATE producto SET precio = %s WHERE producto.id_producto = %s"
                update_query(query,[nuevo_precio,producto_ingresdo])
            elif respuesta == 2:
                nuevo_nombre = str(input("Ingrese el nuevo nombre:"))
                query = "UPDATE producto SET id_producto = %s WHERE producto.id_producto = %s "
                select_query(query,[nuevo_nombre,producto_ingresdo])
            elif respuesta == 3:
                nuevo_nombre = str(input("Ingrese el nuevo nombre:"))
                nuevo_precio = str(input("Ingrese el nuevo precio:"))
                query = "UPDATE producto SET id_producto = %s, precio =%s WHERE producto.id_producto = %s"
                update_query(query,[nuevo_nombre,nuevo_precio,producto_ingresdo])

        print("-----------------------------------------------------------------------------------------")
        print("-----------------------------------------------------------------------------------------")
        continuar = str(input("Desea realizar otra accion? (si/no): "))
        if(continuar.lower() == "si"):
            menu_Administrador()
        elif(continuar.lower() == "no"):
            print("Gracias por utilizar el sistema...saliendo")
            menu = False
            opcion = 7



print("============================================================")
print("=========Bienvenido/a al Negocio de Juanita :D==============")
print()

# *LOGIN APP*
try:
    rut = str(input("Ingrese su rut: "))
    
    
    #caso cliente
    if(rut.lower() != "admin"): 
        query = "SELECT rut FROM cliente WHERE rut = %s"
        resultado = select_query(query,[rut])
       
        #caso de estar en la base de datos
        if (resultado != []): 
            password = str(input("Ingrese su contraseña: "))
            query = "SELECT rut FROM cliente WHERE rut = %s AND pass = %s"
            login = select_query(query,[rut,password])

            #correccion de contraseña
            while (login == []) :
                password = str(input("Error,Ingrese su contraseña nuevamente: "))
                query = "SELECT rut FROM cliente WHERE rut = %s AND pass = %s"
                login = select_query(query,[rut,password]) 
            menu_cliente(rut)

        # verifica si esta registrado o se equivoco en el rut
        else: 
            print("El rut ingresado no existe o esta erroneo...")
            registro = str(input("Esta registrarado? (si/no):"))
            #caso equivocarse en el rut-----------------------------------------------------
            if (registro.lower() == "si" ):
                rut = str(input("Ingrese su rut nuevamente: "))
                query = "SELECT rut FROM cliente WHERE rut = %s "
                resultado = select_query(query,[rut])

                # corrige el rut---------------
                while resultado == []: 
                    rut = str(input("Error,Ingrese su rut nuevamente: "))
                    query = "SELECT rut FROM cliente WHERE rut = %s AND pass = %s"
                    resultado = select_query(query,[rut])

                password = str(input("Ingrese su contraseña: "))
                query = "SELECT rut FROM cliente WHERE rut = %s AND pass = %s"
                login = select_query(query,[rut,password])

                #corrige la contraseña----------
                while (login == []) :
                    password = str(input("Error,Ingrese su contraseña nuevamente: "))
                    query = "SELECT rut FROM cliente WHERE rut = %s AND pass = %s"
                    login = select_query(query,[rut,password]) 
                menu_cliente(rut)   

            #caso nuevo registro
            else: 

                #comienza creando un carrito para el cliente nuevo------------
                query = "SELECT SUM(cant_carritos) FROM (SELECT COUNT(carrito_id) AS cant_carritos FROM carrito GROUP BY carrito_id) AS tabla"
                resultado = select_query(query)
                if resultado[0][0] == None:
                    cant_carritos = 0
                else:
                    cant_carritos = resultado[0][0]
                #ingresa datos del registro-----------------------
                print("Ingrese sus datos para registrarse")
                usuario = str(input("Ingrese su nombre: "))
                carrito_id = cant_carritos + 1
                print("carrito_id:  ",str(carrito_id))
                query = "INSERT INTO carrito (carrito_id) VALUES (%s) "
                insert_query(query,[carrito_id]) 
                password = str(input("Ingrese su contraseña: "))
                saldo = int(input("Ingrese su saldo: "))
                #registra el cliente-----------------------------
                query = "INSERT INTO cliente (usuario,rut,carrito_id,pass,saldo) VALUES (%s,%s,%s,%s,%s)"
                insert_query(query,[usuario,rut,carrito_id,password,saldo])
                print("Se ha registrado correctamente")               
    
    #caso admin
    else:
        password = str(input("Ingrese su contraseña: "))
        while password.lower() != "negociojuanita": #se equivocó en la contraseña
            password = str(input("Error,Ingrese su contraseña nuevamente: "))
        menu_Administrador()

except Exception as error:
    print("Error: %s" % error)

finally:
    print("apagando . . .")
    connection().close()






 