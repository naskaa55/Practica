CREATE TABLE calculations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    expression TEXT NOT NULL,
    result NUMERIC NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_error BOOLEAN DEFAULT FALSE
);

CREATE TABLE calculator_settings (
    user_id INTEGER PRIMARY KEY,
    decimal_places INTEGER DEFAULT 2,
    theme VARCHAR(20) DEFAULT 'light'
);

INSERT INTO calculations (expression, result, is_error) VALUES
    ('2 + 2',            4,       FALSE),
    ('12 + 3 * 4',       24,      FALSE),
    ('100 / 4',          25,      FALSE),
    ('7 * 8',            56,      FALSE),
    ('10 / 0',           0,       TRUE),
    ('(5 + 3) * 2',      16,      FALSE),
    ('3.14 * 2',         6.28,    FALSE);

SELECT * FROM calculations ORDER BY calculated_at DESC LIMIT 10;

SELECT ROUND(AVG(result), 2) AS avg_result FROM calculations WHERE is_error = FALSE;

SELECT COUNT(*) AS errors_count FROM calculations WHERE is_error = TRUE;
