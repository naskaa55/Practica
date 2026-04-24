CREATE TABLE todo_tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    task_text VARCHAR(500) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    priority INTEGER DEFAULT 0,
    category VARCHAR(50)
);

INSERT INTO todo_tasks (task_text, is_completed, priority, category, completed_at) VALUES
    ('Сделать зарядку',                 TRUE,  1, 'здоровье',     CURRENT_TIMESTAMP),
    ('Прочитать книгу',                 FALSE, 0, 'отдых',        NULL),
    ('Купить продукты',                 TRUE,  2, 'быт',          CURRENT_TIMESTAMP),
    ('Сдать практику',                  FALSE, 2, 'учёба',        NULL),
    ('Погулять с собакой',              FALSE, 1, 'быт',          NULL),
    ('Позвонить маме',                  TRUE,  1, 'семья',        CURRENT_TIMESTAMP),
    ('Написать статью',                 FALSE, 2, 'работа',       NULL),
    ('Сходить в спортзал',              FALSE, 1, 'здоровье',     NULL),
    ('Оплатить счета',                  TRUE,  2, 'быт',          CURRENT_TIMESTAMP),
    ('Посмотреть фильм',                FALSE, 0, 'отдых',        NULL);

SELECT * FROM todo_tasks
WHERE is_completed = FALSE
ORDER BY priority DESC, created_at DESC;

UPDATE todo_tasks
SET is_completed = TRUE, completed_at = CURRENT_TIMESTAMP
WHERE id = 5;

SELECT category, is_completed, COUNT(*) AS total
FROM todo_tasks
GROUP BY category, is_completed
ORDER BY category;
