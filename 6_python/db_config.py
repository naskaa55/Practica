"""
Общий файл настроек подключения к PostgreSQL.
"""
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'shop',
    'user': 'postgres',
    'password': 'postgres',
}


def connect():
    """Возвращает соединение с базой."""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn
