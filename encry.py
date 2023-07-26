
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 21:10:41 2023

@author: enigua
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
import os

#función para encriptar los datos a almacenar en MySQL
def encriptar(datos, clave):
    init_v = os.urandom(16)  # Initialization vector de 16 bytes
    padder = padding.PKCS7(128).padder()
    datos_padded = padder.update(datos.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(clave), modes.CFB(init_v), backend=default_backend())
    encriptador = cipher.encryptor()
    datos_encriptados = encriptador.update(datos_padded) + encriptador.finalize()
    return base64.b64encode(init_v + datos_encriptados).decode()