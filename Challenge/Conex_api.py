#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:30:23 2023

@author: enigua
"""

import requests
import pandas as pd

r = requests.get("https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")

if r.status_code == 200:
    result = r.json()
    df = pd.DataFrame(result)
    #print(type (df))
    print(df)
    archivo = open("archivo.txt","w")
else:
    print(f"Error en la solicitud: {r.status_code}")

#result = r.json()
#df = pd.DataFrame(result)
#print(df)