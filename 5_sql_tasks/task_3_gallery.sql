CREATE TABLE gallery_images (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    thumb_url VARCHAR(500) NOT NULL,
    full_url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(200),
    description TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    category VARCHAR(50)
);

INSERT INTO gallery_images (title, thumb_url, full_url, alt_text, description, views, likes, category) VALUES
    ('Горный пейзаж',     'https://picsum.photos/id/10/300/200',  'https://picsum.photos/id/10/1200/800',  'Горы',       'Вид на горы',               120, 15, 'пейзаж'),
    ('Море и закат',      'https://picsum.photos/id/1018/300/200','https://picsum.photos/id/1018/1200/800','Море',       'Закат над морем',            250, 40, 'пейзаж'),
    ('Город ночью',       'https://picsum.photos/id/1019/300/200','https://picsum.photos/id/1019/1200/800','Город',      'Ночной город',                90, 12, 'город'),
    ('Котик',             'https://picsum.photos/id/1025/300/200','https://picsum.photos/id/1025/1200/800','Кот',        'Милый котик',               500, 99, 'животные'),
    ('Собака',            'https://picsum.photos/id/1028/300/200','https://picsum.photos/id/1028/1200/800','Собака',     'Дружелюбная собака',        300, 55, 'животные'),
    ('Лес',               'https://picsum.photos/id/1015/300/200','https://picsum.photos/id/1015/1200/800','Лес',        'Зелёный лес',                60,  7, 'пейзаж'),
    ('Архитектура',       'https://picsum.photos/id/1040/300/200','https://picsum.photos/id/1040/1200/800','Здание',     'Старая архитектура',         40,  5, 'город');

SELECT * FROM gallery_images WHERE category = 'пейзаж' ORDER BY views DESC;

UPDATE gallery_images SET views = views + 1 WHERE id = 4;

SELECT * FROM gallery_images ORDER BY views DESC LIMIT 3;
