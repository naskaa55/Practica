"""
Модуль 4 — TODO.
"""
import csv
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_connect import connect


PRIORITY_NAMES = {0: "низкий", 1: "средний", 2: "высокий"}


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TODO список")
        self.root.geometry("800x550")

        self.filter_var = tk.StringVar(value="all")

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(main)
        left.pack(side="left", fill="both", expand=True)

        # Фильтры
        filters = tk.Frame(left)
        filters.pack(fill="x", pady=5)
        for val, text in [("all", "Все"), ("active", "Активные"), ("done", "Завершённые")]:
            tk.Radiobutton(filters, text=text, variable=self.filter_var,
                           value=val, command=self.load_tasks).pack(side="left", padx=5)

        # Таблица
        self.tree = ttk.Treeview(
            left, columns=("id", "text", "priority", "category", "done"),
            show="headings", height=15
        )
        for col, w in [("id", 40), ("text", 260), ("priority", 80), ("category", 100), ("done", 50)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-Button-1>", self.toggle_complete)

        tk.Button(left, text="Удалить выбранную", command=self.delete_task).pack(pady=5)

        # Правая панель — добавление
        right = tk.Frame(main, relief="ridge", borderwidth=1)
        right.pack(side="right", fill="y", padx=10)

        tk.Label(right, text="Новая задача", font=("Arial", 12, "bold")).pack(pady=10, padx=10)
        tk.Label(right, text="Текст:").pack(anchor="w", padx=10)
        self.text_entry = tk.Entry(right, width=25); self.text_entry.pack(padx=10)

        tk.Label(right, text="Приоритет:").pack(anchor="w", padx=10, pady=(10, 0))
        self.prio_var = tk.IntVar(value=0)
        ttk.Combobox(right, textvariable=self.prio_var, values=[0, 1, 2], width=22).pack(padx=10)

        tk.Label(right, text="Категория:").pack(anchor="w", padx=10, pady=(10, 0))
        self.cat_entry = tk.Entry(right, width=25); self.cat_entry.pack(padx=10)

        tk.Button(right, text="Добавить", command=self.add_task).pack(pady=10)

        # Прогресс + статистика
        self.progress_label = tk.Label(right, text="Завершено: 0%")
        self.progress_label.pack(pady=(10, 0))
        self.progress = ttk.Progressbar(right, length=200, mode="determinate")
        self.progress.pack(pady=5, padx=10)

        self.stats_label = tk.Label(right, text="", justify="left")
        self.stats_label.pack(pady=5, padx=10)

        tk.Button(right, text="Экспорт CSV", command=self.export_csv).pack(pady=2, padx=10, fill="x")
        tk.Button(right, text="Экспорт JSON", command=self.export_json).pack(pady=2, padx=10, fill="x")
        tk.Button(right, text="Импорт CSV", command=self.import_csv).pack(pady=2, padx=10, fill="x")

        self.load_tasks()

    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = connect()
        if not conn: return
        cur = conn.cursor()

        where = ""
        if self.filter_var.get() == "active": where = "WHERE is_completed = FALSE"
        elif self.filter_var.get() == "done": where = "WHERE is_completed = TRUE"

        cur.execute(
            f"SELECT id, task_text, priority, category, is_completed FROM todo_tasks "
            f"{where} ORDER BY priority DESC, created_at DESC"
        )
        for r in cur.fetchall():
            self.tree.insert("", "end", values=(r[0], r[1], PRIORITY_NAMES.get(r[2], r[2]), r[3], "✓" if r[4] else ""))

        # Статистика
        cur.execute("SELECT COUNT(*), SUM(CASE WHEN is_completed THEN 1 ELSE 0 END) FROM todo_tasks")
        total, done = cur.fetchone()
        total = total or 0
        done = done or 0
        pct = (done * 100 / total) if total else 0
        self.progress_label.config(text=f"Завершено: {pct:.0f}%")
        self.progress["value"] = pct

        cur.execute("SELECT category, COUNT(*) FROM todo_tasks GROUP BY category")
        txt = "По категориям:\n"
        for r in cur.fetchall():
            txt += f"  {r[0]}: {r[1]}\n"
        self.stats_label.config(text=txt)
        conn.close()

    def add_task(self):
        text = self.text_entry.get().strip()
        if not text: return
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO todo_tasks (task_text, priority, category) VALUES (%s, %s, %s)",
            (text, self.prio_var.get(), self.cat_entry.get().strip())
        )
        conn.close()
        self.text_entry.delete(0, "end")
        self.cat_entry.delete(0, "end")
        self.load_tasks()

    def toggle_complete(self, event=None):
        sel = self.tree.selection()
        if not sel: return
        values = self.tree.item(sel[0])["values"]
        task_id = values[0]
        is_done = values[4] == "✓"
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        if is_done:
            cur.execute("UPDATE todo_tasks SET is_completed = FALSE, completed_at = NULL WHERE id = %s", (task_id,))
        else:
            cur.execute("UPDATE todo_tasks SET is_completed = TRUE, completed_at = CURRENT_TIMESTAMP WHERE id = %s", (task_id,))
        conn.close()
        self.load_tasks()

    def delete_task(self):
        sel = self.tree.selection()
        if not sel: return
        task_id = self.tree.item(sel[0])["values"][0]
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("DELETE FROM todo_tasks WHERE id = %s", (task_id,))
        conn.close()
        self.load_tasks()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path: return
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT id, task_text, is_completed, priority, category, created_at, completed_at FROM todo_tasks")
        rows = cur.fetchall()
        conn.close()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "text", "completed", "priority", "category", "created_at", "completed_at"])
            for r in rows:
                writer.writerow(r)
        messagebox.showinfo("OK", f"Экспортировано {len(rows)} задач")

    def export_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path: return
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT id, task_text, is_completed, priority, category FROM todo_tasks")
        data = [{"id": r[0], "text": r[1], "done": r[2], "priority": r[3], "category": r[4]} for r in cur.fetchall()]
        conn.close()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("OK", f"Экспортировано {len(data)} задач")

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path: return
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        added = skipped = 0
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("SELECT 1 FROM todo_tasks WHERE task_text = %s", (row["text"],))
                if cur.fetchone():
                    skipped += 1
                    continue
                cur.execute(
                    "INSERT INTO todo_tasks (task_text, priority, category) VALUES (%s, %s, %s)",
                    (row["text"], int(row.get("priority") or 0), row.get("category"))
                )
                added += 1
        conn.close()
        messagebox.showinfo("OK", f"Добавлено: {added}, пропущено: {skipped}")
        self.load_tasks()


if __name__ == "__main__":
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()
