import hashlib
import json
import os
from db_config import connect

CONFIG_FILE = 'config.json'


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def email_exists(email):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
    res = cur.fetchone() is not None
    conn.close()
    return res


def register():
    print("\n-- Регистрация --")
    last = load_last_email()
    email = input(f"Email [{last}]: ").strip() or last
    if not email:
        print("Email обязателен.")
        return
    if email_exists(email):
        print("Email уже зарегистрирован.")
        return
    password = input("Пароль: ").strip()
    full_name = input("Полное имя: ").strip()
    birth_date = input("Дата рождения (YYYY-MM-DD): ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password_hash, full_name, birth_date) "
        "VALUES (%s, %s, %s, %s)",
        (email, hash_password(password), full_name, birth_date)
    )
    print("Пользователь зарегистрирован.")
    conn.close()


def login():
    print("\n-- Вход --")
    last = load_last_email()
    email = input(f"Email [{last}]: ").strip() or last
    password = input("Пароль: ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    if not row or row[1] != hash_password(password):
        print("Неверный email или пароль.")
        conn.close()
        return

    cur.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (row[0],))
    print(f"Успешный вход! id={row[0]}")
    save_last_email(email)
    conn.close()


def list_adults():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, full_name, birth_date FROM users "
        "WHERE birth_date < CURRENT_DATE - INTERVAL '18 years'"
    )
    rows = cur.fetchall()
    print("\nПользователи старше 18:")
    for r in rows:
        print(f"  id={r[0]}  {r[1]}  {r[2]}  род: {r[3]}")
    conn.close()


def save_last_email(email):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({'last_email': email}, f, ensure_ascii=False)


def load_last_email():
    if not os.path.exists(CONFIG_FILE):
        return ''
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('last_email', '')
    except Exception:
        return ''


def main():
    while True:
        print("""
=== Управление пользователями ===
1. Регистрация
2. Вход
3. Список взрослых (18+)
0. Выход
""")
        c = input("Выбор: ").strip()
        if c == '1': register()
        elif c == '2': login()
        elif c == '3': list_adults()
        elif c == '0': break


if __name__ == '__main__':
    main()
