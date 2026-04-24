from db_config import connect


def add_image():
    title = input("Заголовок: ").strip()
    thumb = input("URL миниатюры: ").strip()
    full = input("URL полного изображения: ").strip()
    alt = input("Alt-текст: ").strip()
    description = input("Описание: ").strip()
    category = input("Категория: ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gallery_images (title, thumb_url, full_url, alt_text, description, category) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (title, thumb, full, alt, description, category)
    )
    print("Изображение добавлено.")
    conn.close()


def show_all():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, title, views, category FROM gallery_images ORDER BY views DESC")
    for r in cur.fetchall():
        print(f"  id={r[0]}  {r[1]}  (просмотров: {r[2]}, категория: {r[3]})")
    conn.close()


def increase_views():
    image_id = input("ID изображения: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE gallery_images SET views = views + 1 WHERE id = %s", (image_id,))
    print("Просмотры увеличены.")
    conn.close()


def top_5():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, title, views FROM gallery_images ORDER BY views DESC LIMIT 5")
    print("\nТоп-5 самых популярных:")
    for r in cur.fetchall():
        print(f"  id={r[0]}  {r[1]} — {r[2]} просмотров")
    conn.close()


def filter_category():
    cat = input("Категория: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, title, views FROM gallery_images WHERE category = %s ORDER BY views DESC", (cat,))
    rows = cur.fetchall()
    if not rows:
        print("Ничего не найдено.")
    for r in rows:
        print(f"  id={r[0]}  {r[1]} — {r[2]} просмотров")
    conn.close()


def generate_html():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT title, thumb_url, full_url, alt_text FROM gallery_images")
    rows = cur.fetchall()
    conn.close()

    figures = ""
    for title, thumb, full, alt in rows:
        figures += (
            f'    <figure>\n'
            f'      <img src="{thumb}" data-full="{full}" alt="{alt or title}" loading="lazy">\n'
            f'      <figcaption>{title}</figcaption>\n'
            f'    </figure>\n'
        )

    html = (
        '<!DOCTYPE html>\n<html lang="ru">\n<head>\n'
        '  <meta charset="UTF-8">\n  <title>Галерея</title>\n'
        '  <style>\n'
        '    body { margin: 0; font-family: Arial, sans-serif; background: #222; color: #eee; }\n'
        '    .gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; padding: 20px; }\n'
        '    figure { margin: 0; background: #333; border-radius: 8px; overflow: hidden; }\n'
        '    img { width: 100%; height: 200px; object-fit: cover; display: block; }\n'
        '    figcaption { padding: 10px; text-align: center; }\n'
        '  </style>\n</head>\n<body>\n'
        '  <h1 style="text-align:center">Галерея</h1>\n'
        '  <section class="gallery">\n'
        f'{figures}'
        '  </section>\n'
        '</body>\n</html>\n'
    )

    with open('gallery.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Файл gallery.html создан ({len(rows)} изображений).")


def main():
    while True:
        print("""
=== Управление галереей ===
1. Добавить изображение
2. Показать все (по просмотрам)
3. Увеличить просмотры у изображения
4. Топ-5
5. Фильтр по категории
6. Сгенерировать gallery.html
0. Выход
""")
        c = input("Выбор: ").strip()
        if c == '1': add_image()
        elif c == '2': show_all()
        elif c == '3': increase_views()
        elif c == '4': top_5()
        elif c == '5': filter_category()
        elif c == '6': generate_html()
        elif c == '0': break


if __name__ == '__main__':
    main()
