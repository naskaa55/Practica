"""
Модуль 5 — Калькулятор с историей.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import connect


class CalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("500x600")

        self.expression = ""

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.calc_tab = tk.Frame(notebook, bg="#2b2b2b")
        self.history_tab = tk.Frame(notebook)
        notebook.add(self.calc_tab, text="Калькулятор")
        notebook.add(self.history_tab, text="История")

        self._build_calc()
        self._build_history()

        # Клавиатура
        root.bind("<Key>", self.on_key)

    def _build_calc(self):
        self.display = tk.Label(
            self.calc_tab, text="0", font=("Arial", 28),
            bg="#000", fg="#fff", anchor="e", padx=15, pady=15
        )
        self.display.pack(fill="x", padx=10, pady=10)

        btn_frame = tk.Frame(self.calc_tab, bg="#2b2b2b")
        btn_frame.pack(padx=10, pady=10)

        buttons = [
            ('C', 0, 0, '#c0392b'), ('/', 0, 1, '#e88a1a'),
            ('*', 0, 2, '#e88a1a'), ('-', 0, 3, '#e88a1a'),
            ('7', 1, 0, '#3a3a3a'), ('8', 1, 1, '#3a3a3a'),
            ('9', 1, 2, '#3a3a3a'), ('+', 1, 3, '#e88a1a'),
            ('4', 2, 0, '#3a3a3a'), ('5', 2, 1, '#3a3a3a'),
            ('6', 2, 2, '#3a3a3a'), ('=', 2, 3, '#27ae60'),
            ('1', 3, 0, '#3a3a3a'), ('2', 3, 1, '#3a3a3a'),
            ('3', 3, 2, '#3a3a3a'),
            ('0', 4, 0, '#3a3a3a'), ('.', 4, 2, '#3a3a3a'),
        ]

        for text, row, col, color in buttons:
            colspan = 2 if text == '0' else 1
            rowspan = 2 if text == '=' else 1
            tk.Button(
                btn_frame, text=text, width=6 * colspan, height=2 * rowspan,
                font=("Arial", 14, "bold"), bg=color, fg="white", relief="flat",
                command=lambda t=text: self.press(t)
            ).grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, padx=3, pady=3)

    def _build_history(self):
        top = tk.Frame(self.history_tab)
        top.pack(fill="x", padx=10, pady=10)

        tk.Button(top, text="Обновить", command=self.load_history).pack(side="left", padx=5)
        tk.Button(top, text="Очистить старше 30 дней", command=self.clean_old).pack(side="left", padx=5)

        self.tree = ttk.Treeview(
            self.history_tab, columns=("id", "expr", "result", "err", "at"),
            show="headings"
        )
        for col, w in [("id", 40), ("expr", 140), ("result", 100), ("err", 60), ("at", 140)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.stats_label = tk.Label(self.history_tab, text="")
        self.stats_label.pack(pady=5)

        self.load_history()

    def press(self, value):
        if value == 'C':
            self.expression = ""
        elif value == '=':
            self.calculate()
            return
        else:
            if self.expression == "Ошибка":
                self.expression = ""
            self.expression += value
        self.update_display()

    def update_display(self):
        self.display.config(text=self.expression or "0")

    def calculate(self):
        try:
            safe = ''.join(c for c in self.expression if c in '0123456789+-*/(). ')
            result = eval(safe)
            if isinstance(result, float) and not result.is_integer():
                result = round(result, 6)
            self.save(self.expression, result, False)
            self.expression = str(result)
        except Exception:
            self.save(self.expression, 0, True)
            self.expression = "Ошибка"
        self.update_display()
        self.load_history()

    def save(self, expr, result, is_error):
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO calculations (expression, result, is_error) VALUES (%s, %s, %s)",
            (expr, result, is_error)
        )
        conn.close()

    def load_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute(
            "SELECT id, expression, result, is_error, calculated_at "
            "FROM calculations ORDER BY calculated_at DESC LIMIT 20"
        )
        for r in cur.fetchall():
            self.tree.insert("", "end", values=(r[0], r[1], r[2], "да" if r[3] else "", str(r[4])[:19]))

        cur.execute("SELECT AVG(result), COUNT(*) FILTER (WHERE is_error) FROM calculations")
        avg, errors = cur.fetchone()
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        self.stats_label.config(text=f"Средний результат: {avg_str}   |   Ошибок: {errors or 0}")
        conn.close()

    def clean_old(self):
        if not messagebox.askyesno("Подтверждение", "Удалить записи старше 30 дней?"):
            return
        conn = connect()
        if not conn: return
        cur = conn.cursor()
        cur.execute("DELETE FROM calculations WHERE calculated_at < CURRENT_TIMESTAMP - INTERVAL '30 days'")
        deleted = cur.rowcount
        conn.close()
        messagebox.showinfo("OK", f"Удалено записей: {deleted}")
        self.load_history()

    def on_key(self, event):
        key = event.char
        if key in '0123456789+-*/.':
            self.press(key)
        elif event.keysym == 'Return':
            self.press('=')
        elif event.keysym == 'Escape':
            self.press('C')
        elif event.keysym == 'BackSpace':
            self.expression = self.expression[:-1]
            self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    CalcApp(root)
    root.mainloop()
