#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 06:41:25 2023

@author: enigua
"""
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64
import os

'''La clave secreta para encriptar los valores de las tablas a cifrar 
    (en un entorno real esta clave debe ser custodiada y almacenada en otro lugar de forma segura)
    Genera una sal (puedes utilizar un valor aleatorio único para cada registro)'''
CLAVE_SECRETA = "cl4ve_secreta_123"

def generar_clave(salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    clave = kdf.derive(CLAVE_SECRETA.encode())
    return clave