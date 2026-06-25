# app/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

# Crear el limiter (se usará en rutas y en main)
limiter = Limiter(key_func=get_remote_address)