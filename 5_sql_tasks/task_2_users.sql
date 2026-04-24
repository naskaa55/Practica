CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    birth_date DATE,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_confirmed BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP
);

INSERT INTO users (email, password_hash, full_name, birth_date, is_confirmed) VALUES
    ('ivan@example.com',    'hashed_password_123', 'Иван Петров',     '1995-05-12', TRUE),
    ('anna@example.com',    'hashed_password_123', 'Анна Сидорова',    '2001-09-03', TRUE),
    ('petr@example.com',    'hashed_password_123', 'Пётр Иванов',      '2008-01-20', FALSE),
    ('olga@example.com',    'hashed_password_123', 'Ольга Смирнова',   '1988-11-30', TRUE),
    ('test@example.com',    'hashed_password_123', 'Тест Тестович',    '2000-06-15', FALSE);

SELECT EXISTS(SELECT 1 FROM users WHERE email = 'test@example.com') AS exists;

SELECT * FROM users WHERE birth_date < CURRENT_DATE - INTERVAL '18 years';

UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = 2;
