UPDATE products SET price = 2490.00 WHERE id = 3;

UPDATE products SET is_active = FALSE WHERE stock < 5;

DELETE FROM products WHERE price = 0;

DELETE FROM products WHERE is_active = FALSE AND stock = 0;

UPDATE products SET price = price * 1.10 WHERE name ILIKE '%ноутбук%';
