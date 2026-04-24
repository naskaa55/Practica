import json
from db_config import connect


def save_calc(expression, result, is_error):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO calculations (expression, result, is_error) VALUES (%s, %s, %s)",
        (expression, result, is_error)
    )
    conn.close()


def calculator():
    print("\n-- Калькулятор (пустая строка — выход) --")
    while True:
        expr = input("> ").strip()
        if not expr:
            break
        try:
            safe = ''.join(c for c in expr if c in '0123456789+-*/(). ')
            result = eval(safe)
            print("=", result)
            save_calc(expr, result, False)
        except Exception as e:
            print("Ошибка:", e)
            save_calc(expr, 0, True)


def last_10():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, expression, result, is_error, calculated_at "
        "FROM calculations ORDER BY calculated_at DESC LIMIT 10"
    )
    print("\nПоследние 10 вычислений:")
    for r in cur.fetchall():
        mark = '[ОШИБКА]' if r[3] else ''
        print(f"  id={r[0]}  {r[1]} = {r[2]}  {mark}  ({r[4]})")
    conn.close()


def show_stats():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT AVG(result) FROM calculations WHERE is_error = FALSE")
    avg = cur.fetchone()[0]
    print(f"\nСреднее значение результата: {avg}")

    cur.execute("SELECT COUNT(*) FROM calculations WHERE is_error = TRUE")
    errors = cur.fetchone()[0]
    print(f"Количество ошибок: {errors}")

    print("\nТоп-3 самых частых выражений:")
    cur.execute(
        "SELECT expression, COUNT(*) AS c FROM calculations "
        "GROUP BY expression ORDER BY c DESC LIMIT 3"
    )
    for r in cur.fetchall():
        print(f"  {r[0]} — {r[1]} раз")
    conn.close()


def export_json():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, expression, result, is_error, calculated_at FROM calculations"
    )
    data = []
    for r in cur.fetchall():
        data.append({
            'id': r[0], 'expression': r[1], 'result': float(r[2]) if r[2] is not None else None,
            'is_error': r[3], 'calculated_at': str(r[4]),
        })
    with open('history_export.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Экспортировано {len(data)} записей.")
    conn.close()


def clean_old():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM calculations "
        "WHERE calculated_at < CURRENT_TIMESTAMP - INTERVAL '30 days'"
    )
    print(f"Удалено старых записей: {cur.rowcount}")
    conn.close()


def main():
    while True:
        print("""
=== История калькулятора ===
1. Калькулятор (запись в историю)
2. Последние 10 вычислений
3. Статистика
4. Экспорт в JSON
5. Очистить историю старше 30 дней
0. Выход
""")
        c = input("Выбор: ").strip()
        if c == '1': calculator()
        elif c == '2': last_10()
        elif c == '3': show_stats()
        elif c == '4': export_json()
        elif c == '5': clean_old()
        elif c == '0': break


if __name__ == '__main__':
    main()
