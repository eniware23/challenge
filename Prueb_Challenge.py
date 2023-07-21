#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 20:41:43 2023

@author: enigua
"""

import mysql.connector
import pandas as pd
conexion = mysql.connector.connect(user='root', password='M3RC4D0..P4G0',
                               host='localhost',
                               database='Challenge_mercado_pago',
                               port='3306')
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