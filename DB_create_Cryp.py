#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 21:55:15 2023

@author: enigua
"""
#Importar las librerias que se requieren, "requests" para la conexión tipo GET (solicitud) a la API y mysql.connector para la comunicación con la DB
import requests, datetime, mysql.connector
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os
#función importada desde encriptacion.py para obtener la clave encriptada:
from en_cryp import generar_clave 

#función para encriptar los datos a almacenar en MySQL
def encriptar(datos, clave):
    init_v = os.urandom(16)  # Initialization vector de 16 bytes
    padder = padding.PKCS7(128).padder()
    datos_padded = padder.update(datos.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(clave), modes.CFB(init_v), backend=default_backend())
    encriptador = cipher.encryptor()
    datos_encriptados = encriptador.update(datos_padded) + encriptador.finalize()
    return base64.b64encode(init_v + datos_encriptados).decode()


# Para extraer los datos desde la Appweb Mockapi (API)
url = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error en la solicitud: {response.status_code}")
    exit()


# 'conn' Conexión con la base de datos MySQL y los datos necesarios ya existentes en MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pru3B4..123",
    database="Prueba_123"
    #port="3306"
)
#Creación de un cursor para la interación con la base de datos con el metodo cursor()
cursor = conn.cursor()

#cursor.execute("SHOW DATABASES")

'''Con las siguientes lineas se procede con la creación de las 20 tablas en la base de datos MySQL "Challenge_mercado_pago" 
y se usa un AUTO_INCREMENT para incrementar el identificador por cada tabla creada.'''
#sql = '''ALTER TABLE usuarios ADD COLUMN apellidos VARCHAR(255)''' 
#Sentencia SQL CREATE TABLE
cursor.execute('''CREATE TABLE usuarios
                  (id INT AUTO_INCREMENT PRIMARY KEY,
                   fec_alta DATETIME,
                   user_name VARCHAR(255),
                   codigo_zip VARCHAR(255),
                   credit_card_num VARCHAR(95), 
                   credit_card_ccv VARCHAR(95),
                   cuenta_numero VARCHAR(95),           
                   direccion VARCHAR(255),
                   geo_latitud SMALLINT,
                   geo_longitud SMALLINT,
                   color_favorito VARCHAR(95),
                   foto_dni VARCHAR(255),
                   ip VARCHAR(95),
                   auto VARCHAR(255),
                   auto_modelo VARCHAR(255),
                   auto_tipo VARCHAR(255),
                   auto_color VARCHAR(255),
                   cantidad_compras_realizadas VARCHAR(95),
                   avatar VARCHAR(255),
                   fec_birthday DATETIME)''')


# Mediante las siguientes lineas de realiza la ingesta de los datos en las tablas con el "ciclo For"
for item in data:
    salt = os.urandom(16)    
    id = item.get('id')
    #Desafio 1: convertir la fecha al formato correcto (AAAA-MM-DD HH:MM:SS)
    #fec_alta = datetime.datetime.strptime(item.get('fec_alta'), '%d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S')
    iso_date_fec_alta = item.get('fec_birthday')
    fec_alta = datetime.datetime.fromisoformat(iso_date_fec_alta.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
    user_name = item.get('user_name')
    codigo_zip = item.get('codigo_zip')
    #Desafio 2: el valor a ingresar supera el rango permitido para esta columna.
    credit_card_num = item.get('credit_card_num')
    # Encripta el valor credit_card_ccv
    credit_card_ccv_encriptado = encriptar(item.get('credit_card_ccv'), generar_clave(salt))
    cuenta_numero_encriptado = encriptar(item.get('cuenta_numero'), generar_clave(salt))
    direccion = item.get('direccion')
    geo_latitud = item.get('geo_latitud')
    geo_longitud = item.get('geo_longitud')
    color_favorito_encriptado = encriptar(item.get('color_favorito'), generar_clave(salt))
    foto_dni = item.get('foto_dni')
    ip_encriptado = encriptar(item.get('ip'), generar_clave(salt))
    #ip = item.get('ip')
    auto = item.get('auto')
    auto_modelo = item.get('auto_modelo')
    auto_tipo = item.get('auto_tipo')
    auto_color = item.get('auto_color')
    cantidad_compras_realizadas_encriptado = encriptar(str(item.get('cantidad_compras_realizadas')), generar_clave(salt))
    avatar = item.get('avatar')
    #fec_birthday = item.get('fec_birthday')
    #Desafio 3 es parecido al desafio 1, pero esta vés el formato es de otro tipo...
    #fec_birthday = datetime.datetime.strptime(item.get('fec_birthday'), '%d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S')
    
    # Desafio 3: igual al desafío 1 Formato de fecha "ISO 8601" 
    iso_date_fec_birthday = item.get('fec_birthday')
    # Convertir el formato de fecha ISO 8601 a 'AAAA-MM-DD HH:mm:ss'
    fec_birthday = datetime.datetime.fromisoformat(iso_date_fec_birthday.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO usuarios (fec_alta, user_name, codigo_zip, credit_card_num, credit_card_ccv, cuenta_numero, direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (fec_alta, user_name, codigo_zip, credit_card_num, credit_card_ccv_encriptado, cuenta_numero_encriptado, direccion, geo_latitud, geo_longitud, color_favorito_encriptado, foto_dni, ip_encriptado, auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas_encriptado, avatar, fec_birthday))

#print(cursor.rowcount "registros insertados")
# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
