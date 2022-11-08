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

def verificar_query(query,data=[]):
    try:
        con = connection()
        cursor = con.cursor()
        if con and query != '' and data == []:
            cursor.execute(query)
        elif con and query != '' and data != []: #Con mas parametros 
            cursor.execute(query,data) 
        return True
    except(Exception, Error) as error:
        print("Error: %s" % error)

print("========================================================")
print("=========Bienvenido/a al Negocio de Juanita ===========")
print()

# creaciond de login
try:
    rut = str(input("Ingrese su rut: "))
    if(rut.lower() != "admin"):
        query = "SELECT COUNT(rut) FROM cliente GROUP BY HAVING rut = %s"
        resultado = verificar_query(query,[rut])
        if (resultado == 1): # el rut esta en la base de datos
            password = str(input("Ingrese su contraseña: "))
            query = "SELECT COUNT(rut) FROM cliente GROUP BY rut HAVING rut = %s AND passw = %s"
            login = verificar_query(query,[rut,password])
            while (login == 0) :
                password = str(input("Error,Ingrese su contraseña nuevamente: "))
                query = "SELECT COUNT(rut) FROM cliente GROUP BY rut HAVING rut = %s AND passw = %s"
                login = verificar_query(query,[rut,password]) 
            print("Bienvenido/a al sistema")
        else: # el rut no se encuentra en la base de datos
            print("El rut ingresado no existe o esta erroneo...")
            registro = str(input("Esta registrarado? (si/no):"))
            if registro.lower() == "si": #se equivoco en el rut
                rut = str(input("Ingrese su rut nuevamente: "))
                query = "SELECT * FROM cliente WHERE rut = %s"
                resultado = verificar_query(query,[rut])
                while not resultado:
                    rut = str(input("Error,Ingrese su rut nuevamente: "))
                    query = "SELECT * FROM cliente WHERE rut = %s"
                    resultado = verificar_query(query,[rut])
            else:
                print("Ingrese sus datos para registrarse")
                usuario = str(input("Ingrese su nombre: "))
                rut = str(input("Ingrese su rut: "))
                carrito_id = str(input("Ingrese numero de carrito: "))
                password = str(input("Ingrese su contraseña: "))
                saldo = int(input("Ingrese su saldo: "))
                query = "INSERT INTO cliente (usuario,rut,carrito_id,passw,saldo) VALUES (%s,%s,%s,%s,%s)"
                insert_query(query,[usuario,rut,carrito_id,password,saldo])
                print("Se ha registrado correctamente")

    else:
        password = str(input("Ingrese su contraseña: "))
        while password.lower() != "negociojuanita":
            password = str(input("Error,Ingrese su contraseña nuevamente: "))
        print(".....Bienvenido/a al menu administrador....")
        print("1. Bloquear usuario")
        print("2. Ver el historial de compras")
        print("3. Agregar producto")
        print("4. Actualizar datos de un producto")
        print("5. salir")
        opcion = int(input("Ingrese la opcion que desea realizar: "))
        while opcion != 5:
            if (opcion == 1):
                print("Ingrese el rut del usuario que desea bloquear")

except Exception as error:
    print("Error: %s" % error)






 