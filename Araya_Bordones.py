from asyncio.windows_events import NULL
from logging import error
from pickle import TRUE
from psycopg2 import connect, Error

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



# In[3]
print("========================================================")
print("===============WELCOME TO ESUCELA INGENIERIA :C ========")
print()

rut = str(input("Ingrese su rut: "))
if(rut != "admin" and rut != "ADMIN"): # CLIENTE 
    ingreso = str(input("Eres un nuevo usuario?[y,n]"))
    if(ingreso.lower() == "y"):
        print("REGISTRE LOS SIGUIENTES DATOS: USUARIO, CONTRASEÑA, CARRITO, SALDO")
        usuario = str(input("Ingrese su usuario: "))
        passw = str(input("Ingrese su contraseña: "))
        carrito_id = str(input("Ingrese su numero de carrito: "))
        saldo = str(input("Ingrese su saldo: "))
        query = "insert into cliente(rut, usuario,carrito_id,passw,saldo) values (%s,%s,%s,%s,%s)"
        insert_query(query, (rut,usuario,carrito_id,passw,saldo))
        print("INGRESO DE NUEVA PERSONA EXITOSO Owo")
        connection().close() 
    else:
        print("Le creo ... ")
        passw = str(input("Ingrese su contraseña: ")) 
        query = "select passw  from cliente where passw=%s"
        data, = select_query(query,[passw])[0]
        while(data == None):
            passw = str(input("Ingrese su contraseña: ")) 
            query = "select passw  from cliente where passw=%s"
            data, = select_query(query,[passw])[0] 
        print("INGRESO AL MENU PERSONA EXITOSO Uwu")

else:  #CASO ADMINISTRADOR
    passw = str(input("Ingrese su contraseña: ")) 
    while(passw != "NegocioJuanita"):
        passw = str(input("Ingrese su contraseña: ")) 
    print("BIENVENIDA JUANIAT Uwu")
    