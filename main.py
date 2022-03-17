import os
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


print("---------------------------------------------------------------------------")
def inicio():
    inicio_sesion = int(input("1 para iniciar sesion, 0 para registrarse: "))
    print("---------------------------------------------------------------------------")
    if inicio_sesion == 1:
        return ingresar()
    if inicio_sesion == 0:
        return registro()


def registro():
    global correo
    global contrasena
    nombre = input("ingrese un nombre de usuario: ")
    correo = input("ingrese su correo electronico: ")
    contrasena = input("ingrese su contraseña: ")
    edad = int(input("edad: "))
    ciudad = input("ciudad: ")
    telefono = input("telefono: ")
    print("---------------------------------------------------------------------------")
    con_bd = sqlite3.connect('db.db')
    cursor_db = con_bd.cursor()
    sql = "INSERT INTO usuarios(nombre,correo,contrasena,edad,ciudad,telefono)VALUES(?,?,?,?,?,?)"
    try:
        cursor_db.execute(sql, (nombre,correo,contrasena,edad,ciudad,telefono))
        con_bd.commit()
        return confirmacion_correo(correo)
        cursor_db.close()
    except:
        print("el correo ya existe")


def confirmacion_correo(correo):
    proveedor_correo = 'smtp.gmail.com: 587'
    remitente = 'losdeatras865@gmail.com'
    password = 'adsi86520'

    servidor = smtplib.SMTP(proveedor_correo)
    servidor.starttls()
    servidor.ehlo()
    servidor.login(remitente, password)

    mensaje = "<h1>creaste una una nueva cuenta en ADSI 865</h1>"
    msg = MIMEMultipart()
    msg.attach(MIMEText(mensaje, 'html'))
    msg['From'] = remitente
    msg['To'] = correo
    msg['Subject'] = 'papeleria los de atras'
    servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
    return inicio()


def ingresar():
    correo = input("correo: ")
    contrasena = input("contraseña: ")
    print("---------------------------------------------------------------------------")
    con_bd = sqlite3.connect('db.db')
    cursor_db = con_bd.cursor()
    sql = "SELECT contrasena FROM usuarios WHERE correo ='"+correo+"'and contrasena='"+contrasena+"'"
    cursor_db.execute(sql)
    if cursor_db.fetchall():
        print("ingreso exitoso")
        print("---------------------------------------------------------------------------")

        return productos()
    else:
        print("correo o contraseña invalidos \n INTENTE DE NUEVO... ")
        return ingresar()

total = 0
 
#print(inicio())


#----------------------------------------------------------------------------------------
#productos pagina principal
def productos():

    con_bd = sqlite3.connect('db.db')
    cursor_db = con_bd.cursor()
    sql = "SELECT * FROM productos"
    cursor_db.execute(sql)
    productos = cursor_db.fetchall()
    for fila in productos:
        print(*fila)
    print("---------------------------------------------------------------------------")
    compra = input("ingrese 1 para adquierir productos: ")
    print("---------------------------------------------------------------------------")
    if compra == "1":
        return comprar()
    else:
        return ()
    
def comprar():
    global total
    adquirir = input("ingrese el nombre del producto: ")
    print("---------------------------------------------------------------------------")
    con_bd = sqlite3.connect('db.db')
    cursor_db = con_bd.cursor()
    sql = "SELECT precio FROM productos WHERE nombre_producto='"+adquirir+"'"
    cursor_db.execute(sql)
    consulta=cursor_db.fetchone()
    print(f"{adquirir} tiene un precio de: ",*consulta)
    print("---------------------------------------------------------------------------")
    cantidad = int(input("cuantas unidades desea: "))
    cantidad = cantidad * int(consulta[0])
    print(f"la cantidad de {adquirir} tiene un precio de: ",cantidad)
    print("---------------------------------------------------------------------------")
    total = total + cantidad
    compra = int(input("¿Desea comprar otro producto? (si) ingrese 1 (no) ingrese 0: "))
    print("---------------------------------------------------------------------------")
    if compra == 1:
        return productos()
    else:
        return pagar()

def pagar():
    return f"el valor total a pagar es {total}"


print(inicio())
