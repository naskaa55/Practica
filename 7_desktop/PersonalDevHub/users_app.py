"""
Модуль 2 — Регистрация и авторизация.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import json
import os
from db_connect import connect

TOKEN_FILE = "token.json"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def save_token(email):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump({"email": email}, f)


def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("email")
    except Exception:
        return None


class UsersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход / Регистрация")
        self.root.geometry("450x500")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.login_tab = tk.Frame(self.notebook)
        self.reg_tab = tk.Frame(self.notebook)
        self.list_tab = tk.Frame(self.notebook)

        self.notebook.add(self.login_tab, text="Вход")
        self.notebook.add(self.reg_tab, text="Регистрация")
        self.notebook.add(self.list_tab, text="Пользователи")

        self._build_login()
        self._build_register()
        self._build_list()

        # Авто-вход
        last = load_token()
        if last:
            self.login_email.insert(0, last)

    def _build_login(self):
        tk.Label(self.login_tab, text="Email:").pack(anchor="w", padx=20, pady=(20, 0))
        self.login_email = tk.Entry(self.login_tab)
        self.login_email.pack(fill="x", padx=20)

        tk.Label(self.login_tab, text="Пароль:").pack(anchor="w", padx=20, pady=(10, 0))
        self.login_password = tk.Entry(self.login_tab, show="*")
        self.login_password.pack(fill="x", padx=20)

        tk.Button(self.login_tab, text="Войти", command=self.login).pack(pady=15)
        self.login_status = tk.Label(self.login_tab, text="", fg="green")
        self.login_status.pack()

    def _build_register(self):
        tk.Label(self.reg_tab, text="Email:").pack(anchor="w", padx=20, pady=(15, 0))
        self.reg_email = tk.Entry(self.reg_tab); self.reg_email.pack(fill="x", padx=20)

        tk.Label(self.reg_tab, text="Полное имя:").pack(anchor="w", padx=20, pady=(10, 0))
        self.reg_name = tk.Entry(self.reg_tab); self.reg_name.pack(fill="x", padx=20)

        tk.Label(self.reg_tab, text="Дата рождения (ДД.ММ.ГГГГ):").pack(anchor="w", padx=20, pady=(10, 0))
        self.reg_birth = tk.Entry(self.reg_tab); self.reg_birth.pack(fill="x", padx=20)

        tk.Label(self.reg_tab, text="Пароль:").pack(anchor="w", padx=20, pady=(10, 0))
        self.reg_password = tk.Entry(self.reg_tab, show="*")
        self.reg_password.pack(fill="x", padx=20)
        self.reg_password.bind("<KeyRelease>", self.check_passwords)

        tk.Label(self.reg_tab, text="Повторите пароль:").pack(anchor="w", padx=20, pady=(10, 0))
        self.reg_password2 = tk.Entry(self.reg_tab, show="*")
        self.reg_password2.pack(fill="x", padx=20)
        self.reg_password2.bind("<KeyRelease>", self.check_passwords)

        self.reg_status = tk.Label(self.reg_tab, text="", fg="red")
        self.reg_status.pack(pady=5)

        tk.Button(self.reg_tab, text="Зарегистрироваться", command=self.register).pack(pady=10)

    def _build_list(self):
        tk.Button(self.list_tab, text="Обновить список", command=self.load_users).pack(pady=10)
        self.users_tree = ttk.Treeview(self.list_tab, columns=("id", "email", "name", "birth"), show="headings")
        for col, w in [("id", 40), ("email", 160), ("name", 120), ("birth", 90)]:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=w)
        self.users_tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.load_users()

    def check_passwords(self, event=None):
        if self.reg_password2.get() and self.reg_password.get() != self.reg_password2.get():
            self.reg_status.config(text="Пароли не совпадают", fg="red")
        else:
            self.reg_status.config(text="")

    def login(self):
        email = self.login_email.get().strip()
        password = self.login_password.get()

        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        if not row or row[1] != hash_password(password):
            self.login_status.config(text="Неверный email или пароль", fg="red")
            conn.close()
            return
        cur.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (row[0],))
        conn.close()
        save_token(email)
        self.login_status.config(text=f"Добро пожаловать, id={row[0]}", fg="green")

    def register(self):
        email = self.reg_email.get().strip()
        name = self.reg_name.get().strip()
        birth = self.reg_birth.get().strip()
        pwd = self.reg_password.get()
        pwd2 = self.reg_password2.get()

        if pwd != pwd2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        try:
            d, m, y = birth.split(".")
            birth_sql = f"{y}-{m}-{d}"
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты (ДД.ММ.ГГГГ)")
            return

        conn = connect()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                messagebox.showerror("Ошибка", "Email уже зарегистрирован")
                conn.close()
                return
            cur.execute(
                "INSERT INTO users (email, password_hash, full_name, birth_date) VALUES (%s, %s, %s, %s)",
                (email, hash_password(pwd), name, birth_sql)
            )
            messagebox.showinfo("OK", "Регистрация прошла успешно")
            save_token(email)
            self.load_users()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        conn.close()

    def load_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT id, email, full_name, birth_date FROM users ORDER BY id")
        for row in cur.fetchall():
            self.users_tree.insert("", "end", values=row)
        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    UsersApp(root)
    root.mainloop()
