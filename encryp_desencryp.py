#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 07:10:41 2023

@author: enigua
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
import os

'''La clave secreta para encriptar los valores de las tablas a cifrar 
    (en un entorno real esta clave debe ser custodiada y almacenada en otro lugar de forma segura)
    Genera una sal (puedes utilizar un valor aleatorio único para cada registro)'''

#función para encriptar los datos a almacenar en MySQL
def encriptar(datos, clave):
    init_v = os.urandom(16)  # Initialization vector de 16 bytes
    padder = padding.PKCS7(128).padder()
    datos_padded = padder.update(datos.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(clave), modes.CFB(init_v), backend=default_backend())
    encriptador = cipher.encryptor()
    datos_encriptados = encriptador.update(datos_padded) + encriptador.finalize()
    return base64.b64encode(init_v + datos_encriptados).decode()

def desencriptar(datos_encriptados2, clave2):
    datos_encriptados2 = base64.b64decode(datos_encriptados2)
    init_v = datos_encriptados2[:16]
    datos_encriptados2 = datos_encriptados2[16:]

    cipher = Cipher(algorithms.AES(clave2), modes.CFB(init_v), backend=default_backend())
    desencriptador = cipher.decryptor()
    datos_padded = desencriptador.update(datos_encriptados2) + desencriptador.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    datos = unpadder.update(datos_padded) + unpadder.finalize()
    return datos.decode()