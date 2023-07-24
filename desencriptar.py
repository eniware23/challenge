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

'''La clave secreta para encriptar los valores de las tablas a cifrar 
    (en un entorno real esta clave debe ser custodiada y almacencada en otro lugar de forma segura)
    Genera una sal (puedes utilizar un valor aleatorio único para cada registro)'''

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