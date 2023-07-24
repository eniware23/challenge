#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 20:41:43 2023

@author: enigua
"""

import mysql.connector
import pandas as pd
from mysql.connector import connect
conexion = mysql.connector.connect(user='root', password='M3RC4D0..P4G0',
                               host='localhost',
                               #host='127.0.0.1',
                               database='Challenge_mercado_pago',
                               port='3306',
                               #ssl_ca='/Users/enigua/Library/Application Support/MySQL/Workbench/certificates/1F284704-C5BF-40F0-8985-4942E276A2D7/ca-cert.pem',
                               #ssl_cert='/Users/enigua/Library/Application Support/MySQL/Workbench/certificates/1F284704-C5BF-40F0-8985-4942E276A2D7/client-cert.pem',
                               #ssl_key='/Users/enigua/Library/Application Support/MySQL/Workbench/certificates/1F284704-C5BF-40F0-8985-4942E276A2D7/client-key.pem' 
                               )                                                   
                               
#print(conexion)
cursor = conexion.cursor()
query = '''SELECT user_name, credit_card_num FROM usuarios'''
cursor.execute(query)

#Creación de un cursor para la interacción con la base de datos 
#cursor = conexion.cursor()
#Creación de las tablas en SQL
#sql = """CREATE TABLE clientes (nombre VARCHAR)""".......................................

#cursor.execute(sql) 

#cursor.execute("CREATE DATABASE Challenge_mercado_pago")
#cursor.execute("SHOW DATABASES")
#cursor.execute("SHOW TABLES")
usuarios = cursor.fetchall()
for usuario in usuarios:
    print(usuario)

#conexion.commit()

conexion.close()