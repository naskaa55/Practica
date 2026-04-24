CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(150) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    theme_preference VARCHAR(20) DEFAULT 'light'
);

INSERT INTO blog_posts (title, slug, content, theme_preference, views_count, likes_count) VALUES
    ('Первый пост',        'first-post',     'Привет! Это мой первый пост в блоге.', 'light',  120, 15),
    ('HTML для новичков',  'html-basics',    'Основы HTML за 10 минут.',             'light',   85,  8),
    ('CSS Grid',           'css-grid',       'Что такое CSS Grid и как его использовать.', 'dark', 200, 22),
    ('JavaScript события', 'js-events',      'Как работают события в JS.',           'system', 150, 10),
    ('Тёмная тема',        'dark-theme',     'Как сделать переключатель тёмной темы.', 'dark', 310, 45),
    ('Советы по SQL',      'sql-tips',       'Полезные советы по SQL для новичков.', 'light',   50,  3),
    ('Черновик',           'draft-post',     'Этот пост ещё не опубликован.',        'light',    0,  0);

UPDATE blog_posts SET is_active = FALSE WHERE slug = 'draft-post';

SELECT * FROM blog_posts WHERE is_active = TRUE ORDER BY published_at DESC;

UPDATE blog_posts SET views_count = views_count + 1 WHERE id = 3;

SELECT theme_preference, COUNT(*) AS total FROM blog_posts GROUP BY theme_preference;
