import csv
from db_config import connect


def add_task():
    text = input("Текст задачи: ").strip()
    priority = input("Приоритет (0/1/2): ").strip() or '0'
    category = input("Категория: ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO todo_tasks (task_text, priority, category) VALUES (%s, %s, %s)",
        (text, int(priority), category)
    )
    print("Задача добавлена.")
    conn.close()


def complete_task():
    task_id = input("ID задачи: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE todo_tasks SET is_completed = TRUE, completed_at = CURRENT_TIMESTAMP WHERE id = %s",
        (task_id,)
    )
    print("Задача отмечена завершённой.")
    conn.close()


def show_active():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, task_text, priority, category, created_at FROM todo_tasks "
        "WHERE is_completed = FALSE ORDER BY priority DESC, created_at DESC"
    )
    print("\nНезавершённые задачи:")
    for r in cur.fetchall():
        print(f"  id={r[0]}  [приор {r[2]}] {r[1]}  ({r[3]})")
    conn.close()


def show_stats():
    conn = connect()
    cur = conn.cursor()

    print("\nКоличество задач по категориям:")
    cur.execute("SELECT category, COUNT(*) FROM todo_tasks GROUP BY category")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}")

    cur.execute("SELECT COUNT(*), SUM(CASE WHEN is_completed THEN 1 ELSE 0 END) FROM todo_tasks")
    total, done = cur.fetchone()
    total = total or 0
    done = done or 0
    percent = (done * 100 / total) if total else 0
    print(f"\nВсего задач: {total}, завершено: {done} ({percent:.1f}%)")
    conn.close()


def export_csv():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, task_text, is_completed, priority, category, created_at, completed_at "
        "FROM todo_tasks"
    )
    rows = cur.fetchall()
    conn.close()

    with open('tasks_export.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'text', 'completed', 'priority', 'category', 'created_at', 'completed_at'])
        for r in rows:
            writer.writerow(r)
    print(f"Экспортировано {len(rows)} задач в tasks_export.csv")


def import_csv():
    path = input("Путь к CSV: ").strip() or 'tasks_export.csv'
    try:
        f = open(path, 'r', encoding='utf-8')
    except FileNotFoundError:
        print("Файл не найден.")
        return
    reader = csv.DictReader(f)

    conn = connect()
    cur = conn.cursor()
    added = skipped = 0
    for row in reader:
        cur.execute("SELECT 1 FROM todo_tasks WHERE task_text = %s", (row['text'],))
        if cur.fetchone():
            skipped += 1
            continue
        cur.execute(
            "INSERT INTO todo_tasks (task_text, priority, category) VALUES (%s, %s, %s)",
            (row['text'], int(row.get('priority') or 0), row.get('category'))
        )
        added += 1
    f.close()
    conn.close()
    print(f"Добавлено: {added}, пропущено: {skipped}")


def main():
    while True:
        print("""
=== Управление TODO ===
1. Добавить задачу
2. Отметить завершённой
3. Показать активные
4. Статистика
5. Экспорт в CSV
6. Импорт из CSV
0. Выход
""")
        c = input("Выбор: ").strip()
        if c == '1': add_task()
        elif c == '2': complete_task()
        elif c == '3': show_active()
        elif c == '4': show_stats()
        elif c == '5': export_csv()
        elif c == '6': import_csv()
        elif c == '0': break


if __name__ == '__main__':
    main()
