import json
from db_config import connect


def show_posts_paginated():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM blog_posts WHERE is_active = TRUE")
    total = cur.fetchone()[0]
    per_page = 5
    pages = (total + per_page - 1) // per_page
    if pages == 0:
        print("Постов нет.")
        return

    page = 1
    while True:
        offset = (page - 1) * per_page
        cur.execute(
            "SELECT id, title, slug, views_count FROM blog_posts "
            "WHERE is_active = TRUE ORDER BY published_at DESC LIMIT %s OFFSET %s",
            (per_page, offset)
        )
        rows = cur.fetchall()
        print(f"\n--- Страница {page} из {pages} ---")
        for row in rows:
            print(f"  id={row[0]}  {row[1]} (slug: {row[2]}, просмотров: {row[3]})")
        cmd = input("\n[n] следующая, [p] предыдущая, [q] выход: ").strip().lower()
        if cmd == 'n' and page < pages: page += 1
        elif cmd == 'p' and page > 1:  page -= 1
        elif cmd == 'q': break
    conn.close()


def add_post():
    title = input("Заголовок: ").strip()
    slug = input("Slug (для URL): ").strip()
    content = input("Содержимое: ").strip()
    theme = input("Тема (light/dark/system): ").strip() or 'light'

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO blog_posts (title, slug, content, theme_preference) "
            "VALUES (%s, %s, %s, %s)",
            (title, slug, content, theme)
        )
        print("Пост добавлен!")
    except Exception as e:
        print("Ошибка:", e)
    conn.close()


def increase_views():
    post_id = input("ID поста: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE blog_posts SET views_count = views_count + 1 WHERE id = %s", (post_id,))
    print("Просмотры увеличены.")
    conn.close()


def show_stats():
    conn = connect()
    cur = conn.cursor()

    print("\nТоп-5 самых просматриваемых постов:")
    cur.execute("SELECT id, title, views_count FROM blog_posts ORDER BY views_count DESC LIMIT 5")
    for row in cur.fetchall():
        print(f"  id={row[0]}  {row[1]} — {row[2]} просмотров")

    print("\nКоличество постов по теме:")
    cur.execute("SELECT theme_preference, COUNT(*) FROM blog_posts GROUP BY theme_preference")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
    conn.close()


def export_json():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, slug, content, published_at, is_active, "
        "views_count, likes_count, theme_preference FROM blog_posts"
    )
    posts = []
    for row in cur.fetchall():
        posts.append({
            'id': row[0], 'title': row[1], 'slug': row[2], 'content': row[3],
            'published_at': str(row[4]), 'is_active': row[5],
            'views_count': row[6], 'likes_count': row[7], 'theme_preference': row[8],
        })
    with open('posts_export.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"Экспортировано {len(posts)} постов в posts_export.json")
    conn.close()


def import_json():
    path = input("Путь к файлу JSON: ").strip() or 'posts_export.json'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print("Файл не найден.")
        return

    conn = connect()
    cur = conn.cursor()
    added = skipped = 0
    for p in posts:
        cur.execute("SELECT 1 FROM blog_posts WHERE slug = %s", (p['slug'],))
        if cur.fetchone():
            skipped += 1
            continue
        cur.execute(
            "INSERT INTO blog_posts (title, slug, content, theme_preference) "
            "VALUES (%s, %s, %s, %s)",
            (p['title'], p['slug'], p['content'], p.get('theme_preference', 'light'))
        )
        added += 1
    print(f"Добавлено: {added}, пропущено (slug уже есть): {skipped}")
    conn.close()


def main():
    while True:
        print("""
=== Управление блогом ===
1. Показать активные посты
2. Добавить пост
3. Увеличить просмотры у поста
4. Статистика
5. Экспорт в JSON
6. Импорт из JSON
0. Выход
""")
        c = input("Выбор: ").strip()
        if c == '1': show_posts_paginated()
        elif c == '2': add_post()
        elif c == '3': increase_views()
        elif c == '4': show_stats()
        elif c == '5': export_json()
        elif c == '6': import_json()
        elif c == '0': break


if __name__ == '__main__':
    main()
