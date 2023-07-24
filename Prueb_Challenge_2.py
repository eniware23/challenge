#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 20:41:43 2023

@author: enigua
"""

import mysql.connector, pandas as pd
from mysql.connector import connect
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os
#función importada desde encriptacion.py para obtener la clave encriptada:
from encriptacion import generar_clave 

conexion = mysql.connector.connect(user='root', password='M3RC4D0..P4G0',
                               host='localhost',
                               #host='127.0.0.1',
                               database='Challenge_mercado_pago',
                               port='3306',
                               #ssl_ca='/Users/enigua/Library/Application Support/MySQL/Workbench/certificates/1F284704-C5BF-40F0-8985-4942E276A2D7/ca-cert.pem',
                               #ssl_cert='/Users/enigua/Library/Application Support/MySQL/Workbench/certificates/1F284704-C5BF-40F0-8985-4942E276A2D7/client-cert.pem',
                               #ssl_key='/Users/enigua/Library/Application Support/MySQL/Workbench/certificates/1F284704-C5BF-40F0-8985-4942E276A2D7/client-key.pem' 
                               )                                                   
# Creación de un cursor para la interacción con la base de datos con el método cursor()
id_usuario = 33
cursor = conexion.cursor()
cursor.execute("SELECT credit_card_ccv FROM usuarios WHERE id = %s", (id_usuario,))
#cursor.execute('''SELECT user_name, credit_card_ccv FROM usuarios''')
resultado = cursor.fetchone()


def desencriptar(datos_encriptados, clave):
    datos_encriptados = base64.b64decode(datos_encriptados)
    init_v = datos_encriptados[:16]
    datos_encriptados = datos_encriptados[16:]

    cipher = Cipher(algorithms.AES(clave), modes.CFB(init_v), backend=default_backend())
    desencriptador = cipher.decryptor()
    datos_padded = desencriptador.update(datos_encriptados) + desencriptador.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    datos = unpadder.update(datos_padded) + unpadder.finalize()
    return datos.decode()


if resultado:
    resultado = resultado[0]
    # Desencriptar el campo credit_card_ccv
    credit_card_ccv = desencriptar(resultado, clave_encriptacion)
    print("Credit Card CCV desencriptado:", credit_card_ccv)
else:
    print("Usuario no encontrado")

conexion.close()