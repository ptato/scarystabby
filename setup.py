#!/usr/bin/env python3
from distutils.core import setup, Extension

# C Extension Module
dd_module = Extension ( 
      name = 'dd'
    , sources = ['ddmodule.c']
    , language = 'c'
)

setup ( 
      name = 'scarystabby'
    , description = 'Devil Daggers Private Server'
    , version = '0.1'

    , author = 'Pablo Tato'
    , url = 'https://github.com/ptato/scarystabby'

    , ext_modules = [dd_module]
    , scripts = ['server.py']
)
