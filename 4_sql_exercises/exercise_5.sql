ALTER TABLE products ADD COLUMN IF NOT EXISTS category VARCHAR(50);

UPDATE products SET category = 'ноутбуки'   WHERE name ILIKE '%ноутбук%';
UPDATE products SET category = 'периферия'  WHERE name ILIKE '%мышь%' OR name ILIKE '%клавиатура%' OR name ILIKE '%коврик%';
UPDATE products SET category = 'мониторы'   WHERE name ILIKE '%монитор%';
UPDATE products SET category = 'аудио'      WHERE name ILIKE '%наушники%';
UPDATE products SET category = 'видео'      WHERE name ILIKE '%веб-камера%';

-- 1. Сколько всего товаров
SELECT COUNT(*) AS total FROM products;

-- 2. Сколько активных
SELECT COUNT(*) AS active_total FROM products WHERE is_active = TRUE;

-- 3. Общая стоимость склада
SELECT SUM(price * stock) AS total_value FROM products;

-- 4. Средняя цена
SELECT AVG(price) AS avg_price FROM products;

-- 5. Самый дорогой и самый дешёвый товар
SELECT MAX(price) AS max_price, MIN(price) AS min_price FROM products;

-- 6. Количество товаров по статусу активности
SELECT is_active, COUNT(*) AS total FROM products GROUP BY is_active;

-- 7. Сумма товаров на складе по категориям
SELECT category, SUM(stock) AS total_stock FROM products GROUP BY category;
