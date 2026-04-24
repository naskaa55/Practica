import subprocess
import sys
import os
import tkinter as tk
from tkinter import messagebox

HERE = os.path.dirname(os.path.abspath(__file__))


def run_module(filename):
    path = os.path.join(HERE, filename)
    try:
        subprocess.Popen([sys.executable, path])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить {filename}: {e}")


def main():
    root = tk.Tk()
    root.title("PersonalDevHub")
    root.geometry("420x520")
    root.configure(bg="#2c3e50")

    tk.Label(
        root, text="PersonalDevHub",
        font=("Arial", 22, "bold"), bg="#2c3e50", fg="white"
    ).pack(pady=20)
    tk.Label(
        root, text="Главное меню",
        font=("Arial", 12), bg="#2c3e50", fg="#bdc3c7"
    ).pack(pady=(0, 20))

    buttons = [
        ("Блог",               "blog_app.py",    "#3498db"),
        ("Пользователи",       "users_app.py",   "#9b59b6"),
        ("Галерея",            "gallery_app.py", "#e67e22"),
        ("TODO",               "todo_app.py",    "#27ae60"),
        ("Калькулятор",        "calc_app.py",    "#e74c3c"),
    ]

    for text, module, color in buttons:
        tk.Button(
            root, text=text, font=("Arial", 14, "bold"),
            bg=color, fg="white", width=25, height=2,
            relief="flat", activebackground=color,
            command=lambda m=module: run_module(m)
        ).pack(pady=5)

    tk.Button(
        root, text="Выход", font=("Arial", 10),
        bg="#7f8c8d", fg="white", width=15,
        command=root.destroy
    ).pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
