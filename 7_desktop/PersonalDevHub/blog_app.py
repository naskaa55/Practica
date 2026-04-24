"""
Модуль 1 — Блог.
Список постов, чтение, создание, тема, пагинация, поиск, статистика.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_connect import connect

POSTS_PER_PAGE = 5


class BlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Мой блог")
        self.root.geometry("700x550")

        self.is_dark = False
        self.current_page = 1
        self.search_query = ""

        self._build_ui()
        self.load_posts()

    def _build_ui(self):
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=10, pady=10)

        tk.Label(top, text="Поиск:").pack(side="left")
        self.search_var = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.search_var, width=25)
        entry.pack(side="left", padx=5)
        entry.bind("<KeyRelease>", self.on_search)

        tk.Button(top, text="Новый пост", command=self.new_post).pack(side="left", padx=5)
        tk.Button(top, text="Тема", command=self.toggle_theme).pack(side="right")

        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(fill="both", expand=True, padx=10)

        pag = tk.Frame(self.root)
        pag.pack(pady=5)
        tk.Button(pag, text="< Назад", command=self.prev_page).pack(side="left", padx=5)
        self.page_label = tk.Label(pag, text="1")
        self.page_label.pack(side="left")
        tk.Button(pag, text="Вперёд >", command=self.next_page).pack(side="left", padx=5)

        self.stats_label = tk.Label(self.root, text="")
        self.stats_label.pack(pady=5)

    def on_search(self, event=None):
        self.search_query = self.search_var.get()
        self.current_page = 1
        self.load_posts()

    def load_posts(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        conn = connect()
        if not conn: return
        cur = conn.cursor()

        where = "is_active = TRUE"
        params = []
        if self.search_query:
            where += " AND title ILIKE %s"
            params.append(f"%{self.search_query}%")

        cur.execute(f"SELECT COUNT(*) FROM blog_posts WHERE {where}", params)
        total = cur.fetchone()[0]
        offset = (self.current_page - 1) * POSTS_PER_PAGE

        cur.execute(
            f"SELECT id, title, published_at, content, views_count FROM blog_posts "
            f"WHERE {where} ORDER BY published_at DESC LIMIT %s OFFSET %s",
            params + [POSTS_PER_PAGE, offset]
        )

        for row in cur.fetchall():
            post_id, title, date, content, views = row
            short = (content[:100] + "...") if len(content) > 100 else content
            item = tk.Frame(self.list_frame, relief="ridge", borderwidth=1)
            item.pack(fill="x", pady=3)
            tk.Label(item, text=title, font=("Arial", 12, "bold"), anchor="w").pack(fill="x", padx=5)
            tk.Label(item, text=f"{date}", fg="gray", anchor="w").pack(fill="x", padx=5)
            tk.Label(item, text=short, anchor="w", wraplength=650, justify="left").pack(fill="x", padx=5)
            tk.Button(item, text="Читать", command=lambda pid=post_id: self.read_post(pid)).pack(anchor="e", padx=5, pady=3)

        self.page_label.config(text=f"Стр {self.current_page}")

        cur.execute("SELECT COUNT(*), COALESCE(SUM(views_count), 0) FROM blog_posts")
        total_posts, total_views = cur.fetchone()
        self.stats_label.config(text=f"Всего постов: {total_posts}, просмотров всего: {total_views}")
        conn.close()

    def read_post(self, post_id):
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("UPDATE blog_posts SET views_count = views_count + 1 WHERE id = %s", (post_id,))
        cur.execute("SELECT title, content, published_at FROM blog_posts WHERE id = %s", (post_id,))
        row = cur.fetchone()
        conn.close()

        if not row: return
        title, content, date = row

        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("600x400")
        tk.Label(win, text=title, font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(win, text=str(date), fg="gray").pack()
        txt = tk.Text(win, wrap="word", padx=10, pady=10)
        txt.insert("1.0", content)
        txt.config(state="disabled")
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_posts()

    def new_post(self):
        win = tk.Toplevel(self.root)
        win.title("Новый пост")
        win.geometry("500x450")

        tk.Label(win, text="Заголовок:").pack(anchor="w", padx=10, pady=(10, 0))
        title_e = tk.Entry(win); title_e.pack(fill="x", padx=10)

        tk.Label(win, text="Slug:").pack(anchor="w", padx=10, pady=(10, 0))
        slug_e = tk.Entry(win); slug_e.pack(fill="x", padx=10)

        tk.Label(win, text="Содержимое:").pack(anchor="w", padx=10, pady=(10, 0))
        content_t = tk.Text(win, height=10); content_t.pack(fill="both", expand=True, padx=10)

        tk.Label(win, text="Тема:").pack(anchor="w", padx=10, pady=(10, 0))
        theme_v = tk.StringVar(value="light")
        ttk.Combobox(win, textvariable=theme_v, values=["light", "dark", "system"]).pack(fill="x", padx=10)

        def save():
            conn = connect()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO blog_posts (title, slug, content, theme_preference) VALUES (%s, %s, %s, %s)",
                    (title_e.get(), slug_e.get(), content_t.get("1.0", "end").strip(), theme_v.get())
                )
                messagebox.showinfo("OK", "Пост добавлен")
                win.destroy()
                self.load_posts()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            conn.close()

        tk.Button(win, text="Сохранить", command=save).pack(pady=10)

    def next_page(self):
        self.current_page += 1
        self.load_posts()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_posts()

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        bg, fg = ("#1e1e1e", "#eee") if self.is_dark else ("#ffffff", "#000")
        self._apply_theme(self.root, bg, fg)

    def _apply_theme(self, widget, bg, fg):
        try: widget.configure(bg=bg)
        except tk.TclError: pass
        for child in widget.winfo_children():
            try:
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.configure(bg=bg)
                if isinstance(child, tk.Label):
                    child.configure(fg=fg)
            except tk.TclError: pass
            self._apply_theme(child, bg, fg)


if __name__ == "__main__":
    root = tk.Tk()
    BlogApp(root)
    root.mainloop()
