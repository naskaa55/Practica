"""
Модуль 3 — Галерея.
Сетка миниатюр, клик открывает большое изображение.
"""
import io
import tkinter as tk
from tkinter import ttk, messagebox
from urllib.request import urlopen
from PIL import Image, ImageTk
from db_connect import connect


class GalleryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Галерея")
        self.root.geometry("800x600")

        self.images = []
        self.thumb_cache = {}

        top = tk.Frame(root)
        top.pack(fill="x", padx=10, pady=10)

        tk.Label(top, text="Категория:").pack(side="left")
        self.cat_var = tk.StringVar(value="Все")
        self.cat_combo = ttk.Combobox(top, textvariable=self.cat_var, state="readonly")
        self.cat_combo.pack(side="left", padx=5)
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self.load_images())

        tk.Button(top, text="Добавить фото", command=self.add_image).pack(side="left", padx=5)
        tk.Button(top, text="Топ по просмотрам", command=self.show_top).pack(side="left", padx=5)

        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.load_categories()
        self.load_images()

    def load_categories(self):
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT category FROM gallery_images WHERE category IS NOT NULL")
        cats = ["Все"] + [r[0] for r in cur.fetchall()]
        self.cat_combo["values"] = cats
        conn.close()

    def load_images(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        conn = connect()
        if not conn: return
        cur = conn.cursor()
        if self.cat_var.get() == "Все":
            cur.execute("SELECT id, title, thumb_url, full_url, views FROM gallery_images ORDER BY id")
        else:
            cur.execute(
                "SELECT id, title, thumb_url, full_url, views FROM gallery_images WHERE category = %s ORDER BY id",
                (self.cat_var.get(),)
            )
        self.images = cur.fetchall()
        conn.close()

        cols = 3
        for idx, (img_id, title, thumb, full, views) in enumerate(self.images):
            frame = tk.Frame(self.grid_frame, relief="ridge", borderwidth=1, padx=5, pady=5)
            frame.grid(row=idx // cols, column=idx % cols, padx=5, pady=5)

            photo = self._load_thumb(thumb)
            if photo:
                lbl = tk.Label(frame, image=photo, cursor="hand2")
                lbl.image = photo
                lbl.pack()
                lbl.bind("<Button-1>", lambda e, i=idx: self.open_full(i))
            tk.Label(frame, text=title).pack()
            tk.Label(frame, text=f"Просмотров: {views}", fg="gray").pack()

    def _load_thumb(self, url):
        if url in self.thumb_cache:
            return self.thumb_cache[url]
        try:
            data = urlopen(url, timeout=5).read()
            img = Image.open(io.BytesIO(data))
            img.thumbnail((200, 150))
            photo = ImageTk.PhotoImage(img)
            self.thumb_cache[url] = photo
            return photo
        except Exception:
            return None

    def open_full(self, index):
        img_id, title, thumb, full, _ = self.images[index]
        # Увеличиваем просмотры
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute("UPDATE gallery_images SET views = views + 1 WHERE id = %s", (img_id,))
            conn.close()

        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("900x650")

        lbl = tk.Label(win, text="Загрузка...")
        lbl.pack(expand=True)

        def load_full():
            try:
                data = urlopen(full, timeout=10).read()
                img = Image.open(io.BytesIO(data))
                img.thumbnail((850, 600))
                photo = ImageTk.PhotoImage(img)
                lbl.configure(image=photo, text="")
                lbl.image = photo
                # fade-in: плавно поднимаем прозрачность через attributes alpha
                for i in range(1, 11):
                    win.attributes("-alpha", i / 10)
                    win.update()
                    win.after(20)
            except Exception as e:
                lbl.configure(text=f"Ошибка: {e}")

        nav = tk.Frame(win)
        nav.pack(pady=5)

        def prev_img():
            win.destroy()
            self.open_full((index - 1) % len(self.images))

        def next_img():
            win.destroy()
            self.open_full((index + 1) % len(self.images))

        tk.Button(nav, text="< Назад", command=prev_img).pack(side="left", padx=10)
        tk.Button(nav, text="Вперёд >", command=next_img).pack(side="left", padx=10)

        win.after(100, load_full)
        self.load_images()

    def add_image(self):
        win = tk.Toplevel(self.root)
        win.title("Добавить фото")
        win.geometry("400x400")

        fields = {}
        for label_text in ["Заголовок", "URL миниатюры", "URL полного", "Alt-текст", "Описание", "Категория"]:
            tk.Label(win, text=label_text + ":").pack(anchor="w", padx=10, pady=(5, 0))
            e = tk.Entry(win)
            e.pack(fill="x", padx=10)
            fields[label_text] = e

        def save():
            conn = connect()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO gallery_images (title, thumb_url, full_url, alt_text, description, category) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (fields["Заголовок"].get(), fields["URL миниатюры"].get(),
                     fields["URL полного"].get(), fields["Alt-текст"].get(),
                     fields["Описание"].get(), fields["Категория"].get())
                )
                messagebox.showinfo("OK", "Изображение добавлено")
                win.destroy()
                self.load_categories()
                self.load_images()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            conn.close()

        tk.Button(win, text="Сохранить", command=save).pack(pady=15)

    def show_top(self):
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT title, views FROM gallery_images ORDER BY views DESC LIMIT 5")
        msg = "Топ-5 по просмотрам:\n\n" + "\n".join(f"{t} — {v}" for t, v in cur.fetchall())
        conn.close()
        messagebox.showinfo("Топ", msg)


if __name__ == "__main__":
    root = tk.Tk()
    GalleryApp(root)
    root.mainloop()
