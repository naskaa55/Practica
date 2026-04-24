INSERT INTO products (name, price, stock, is_active) VALUES
    ('Ноутбук Lenovo',          84990.00, 12, TRUE),
    ('Мышь Logitech',             1890.50, 45, TRUE),
    ('Клавиатура механическая',      0.00,  0, FALSE),
    ('Монитор 27" Dell',         16500.00,  3, TRUE),
    ('Наушники Sony',             5990.00, 20, TRUE),
    ('Ноутбук HP',               54990.00,  7, TRUE),
    ('Коврик для мыши',             390.00, 0, TRUE),
    ('Веб-камера Logitech',       3490.00, 15, TRUE);

-- 1. Все товары
SELECT * FROM products;

-- 2. Название и цена, сортировка по цене убыв.
SELECT name, price FROM products ORDER BY price DESC;

-- 3. Только те, где stock > 0
SELECT * FROM products WHERE stock > 0;

-- 4. Только активные, сортировка по имени
SELECT * FROM products WHERE is_active = TRUE ORDER BY name;

-- 5. Цена = 0 ИЛИ stock = 0
SELECT * FROM products WHERE price = 0 OR stock = 0;
