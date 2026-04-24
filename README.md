# Практика

---

## Содержание

1. [Структура проекта](#структура-проекта)
2. [Установка Python](#1-установка-python)
3. [Установка Docker](#2-установка-docker)
4. [Настройка PostgreSQL в Docker](#3-настройка-postgresql-в-docker)
5. [Альтернатива — локальная установка PostgreSQL](#4-альтернатива--локальная-установка-postgresql)
6. [Установка зависимостей Python](#5-установка-зависимостей-python)
7. [Запуск SQL-заданий](#6-запуск-sql-заданий)
8. [Запуск Python-скриптов](#7-запуск-python-скриптов)
9. [Запуск десктопного приложения](#8-запуск-десктопного-приложения-personaldevhub)
10. [HTML / CSS / JS](#9-html--css--js)
11. [Решение частых проблем](#10-решение-частых-проблем)

---

## Структура проекта

```
solutions/
├── 1_html/             — HTML (5 страниц)
├── 2_css/              — CSS для этих страниц
├── 3_js/               — JavaScript для этих страниц
├── 4_sql_exercises/    — SQL упражнения 1–5 (таблица products)
├── 5_sql_tasks/        — SQL задания 1–5 (блог, юзеры, галерея, TODO, калькулятор)
├── 6_python/           — Python-скрипты (консольные)
└── 7_desktop/          — Десктопное приложение PersonalDevHub
```

---

## 1. Установка Python

Требуется **Python 3.10 или новее**.

### Windows

1. Скачай инсталлятор с официального сайта: https://www.python.org/downloads/windows/
2. Запусти `.exe` файл.
3. **ВАЖНО:** на первом экране поставь галочку **«Add Python to PATH»**.
4. Нажми **«Install Now»**.
5. Проверь установку, открыв PowerShell или cmd:
   ```bash
   python --version
   pip --version
   ```
   Должно вывести что-то вроде `Python 3.12.x` и `pip 24.x`.

### macOS

```bash
brew install python@3.12
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Создание виртуального окружения (рекомендуется)

Чтобы не ставить пакеты глобально:

```bash
# в корне проекта
python -m venv venv

# активация (Windows)
venv\Scripts\activate

# активация (macOS/Linux)
source venv/bin/activate
```

После активации в начале строки появится `(venv)` — значит всё работает.

---

## 2. Установка Docker

### Windows 10/11

1. Скачай **Docker Desktop** с https://www.docker.com/products/docker-desktop/
2. Перед установкой убедись, что включён **WSL 2**:
   ```powershell
   wsl --install
   ```
   (перезагрузи ПК если потребуется)
3. Запусти инсталлятор Docker Desktop, оставь настройки по умолчанию (должна быть галочка «Use WSL 2 instead of Hyper-V»).
4. После установки перезагрузись и запусти **Docker Desktop** — дождись появления зелёного значка «Running».
5. Проверь в PowerShell:
   ```bash
   docker --version
   docker run hello-world
   ```

### macOS

1. Скачай Docker Desktop для Mac (Intel/Apple Silicon) с того же сайта.
2. Перетащи в «Программы», запусти, дождись иконки в меню-баре.
3. Проверь: `docker --version`.

### Linux (Ubuntu)

```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER   # чтоб запускать без sudo
# перелогинься
docker --version
```

---

## 3. Настройка PostgreSQL в Docker

Самый быстрый способ — запустить PostgreSQL в контейнере.

### Вариант А — одной командой

```bash
docker run -d ^
  --name pg-practica ^
  -e POSTGRES_USER=postgres ^
  -e POSTGRES_PASSWORD=postgres ^
  -e POSTGRES_DB=shop ^
  -p 5432:5432 ^
  -v pgdata:/var/lib/postgresql/data ^
  postgres:16
```

**Параметры:**
- `-d` — запуск в фоне
- `--name pg-practica` — имя контейнера
- `-e POSTGRES_*` — логин / пароль / имя БД
- `-p 5432:5432` — проброс порта наружу
- `-v pgdata:/var/lib/postgresql/data` — том для сохранения данных между перезапусками

### Вариант Б — через docker-compose.yml

Создай файл `docker-compose.yml` в корне проекта:

```yaml
version: "3.9"
services:
  postgres:
    image: postgres:16
    container_name: pg-practica
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: shop
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Запуск:

```bash
docker compose up -d
```

Остановка: `docker compose down` (данные сохраняются в томе `pgdata`).

### Проверка, что PostgreSQL работает

```bash
docker ps                       # должен быть контейнер pg-practica
docker logs pg-practica         # последние строки «database system is ready to accept connections»
docker exec -it pg-practica psql -U postgres -d shop
```

Внутри psql:
```sql
\l        -- список баз, должна быть shop
\q        -- выход
```

### Подключение через GUI (опционально)

Установи **pgAdmin 4** (https://www.pgadmin.org/) или **DBeaver** (https://dbeaver.io/) и создай подключение с параметрами:

| Параметр | Значение   |
|----------|------------|
| Host     | localhost  |
| Port     | 5432       |
| Database | shop       |
| User     | postgres   |
| Password | postgres   |

---

## 4. Альтернатива — локальная установка PostgreSQL

Если Docker использовать не хочется:

### Windows
1. Скачай установщик: https://www.postgresql.org/download/windows/
2. Запусти, укажи пароль пользователя `postgres` (запомни!).
3. Порт оставь `5432`.
4. В pgAdmin создай базу `shop`:
   ```sql
   CREATE DATABASE shop;
   ```

### macOS
```bash
brew install postgresql@16
brew services start postgresql@16
createdb shop
```

### Linux
```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE DATABASE shop;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

---

## 5. Установка зависимостей Python

Из корня проекта (если создавал venv — активируй его):

```bash
pip install psycopg2-binary pillow
```

Либо для десктопного приложения — через `requirements.txt`:

```bash
cd 7_desktop/PersonalDevHub
pip install -r requirements.txt
```

---

## 6. Запуск SQL-заданий



### Через Docker (psql внутри контейнера)

```bash
docker exec -i pg-practica psql -U postgres -d shop < 4_sql_exercises/exercise_1.sql
```

### Через pgAdmin / DBeaver
Откройте `.sql` файл в Query Tool, выполни (F5).


---

## 7. Запуск Python-скриптов

Перед запуском проверь `6_python/db_config.py` — параметры должны совпадать с теми, с которыми запущена PostgreSQL:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'shop',
    'user': 'postgres',
    'password': 'postgres',
}
```

Запуск:

```bash
cd 6_python
python 1_blog_manager.py
python 2_users_manager.py
python 3_gallery_manager.py
python 4_todo_manager.py
python 5_calc_history.py
```

У каждого скрипта — текстовое меню в консоли.

---

## 8. Запуск десктопного приложения PersonalDevHub

```bash
cd 7_desktop/PersonalDevHub
pip install -r requirements.txt
python main.py
```

Параметры подключения — в `db_connect.py` (должны совпадать с PostgreSQL).

### Сборка в .exe (опционально)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
