"""
Общий модуль подключения к PostgreSQL.
"""
import psycopg2
from tkinter import messagebox

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'shop',
    'user': 'postgres',
    'password': 'postgres',
}


def connect():
    """Открывает соединение. При ошибке показывает messagebox."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        return conn
    except Exception as e:
        messagebox.showerror("Ошибка подключения к БД", str(e))
        return None
