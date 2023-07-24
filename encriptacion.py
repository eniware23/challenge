#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 06:41:25 2023

@author: enigua
"""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

def generar_clave(secret_key, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    clave = kdf.derive(secret_key.encode())
    return clave

def clave_encriptacion():
    clave_secreta = "cl4ve_secreta_123"
    salt = os.urandom(16)
    clave_encriptacion = generar_clave(clave_secreta, salt)