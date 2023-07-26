#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 20:41:43 2023

@author: enigua
"""

import mysql.connector
from mysql.connector import connect
import os
#función importada desde encriptacion.py para obtener la clave encriptada:
from encryp_desencryp import desencriptar
from clave import generar_clave
conexion = mysql.connector.connect(user='root', password='Pru3B4..123',
                                   host='localhost',
                                   #host='127.0.0.1',
                                   database="Prueba_123",
                                   port='3306',
                                   )                                                   
# Creación de un cursor para la interacción con la base de datos con el método cursor()
id_usuario = 33
cursor = conexion.cursor()
cursor.execute("SELECT credit_card_ccv FROM usuarios WHERE id = %s", (id_usuario,))
#cursor.execute('''SELECT user_name, credit_card_ccv FROM usuarios''')
resultado = cursor.fetchone()

CLAVE_SECRETA = "cl4ve_secreta_123"
salt = os.urandom(16)

clave_encriptacion = generar_clave(salt)

if resultado:
    datos_encriptados = resultado[0]     
    # Desencriptar los datos utilizando la clave secreta 
    datos_desencriptados = desencriptar(datos_encriptados, clave_encriptacion)      
    
    print("Credit Card CCV desencriptado:", datos_desencriptados)
else:
    print("Usuario no encontrado")

conexion.close()
