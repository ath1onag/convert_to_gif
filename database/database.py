import aiomysql
from config_data.config import MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
import logging

pool = None


async def get_db_connection():
    """Создает асинхронное подключение к базе данных MySQL"""
    connection = await aiomysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DATABASE
    )
    return connection

async def create_table():
    """Создаем таблицу пользователей в базе данных"""
    connection = await get_db_connection()
    async with connection.cursor() as cursor:
        await cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id BIGINT NOT NULL,
                                username VARCHAR(255),
                                joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )''')
    pass
    connection.close()

async def insert_user(user_id, username):
    """Добавляем нового пользователя в базу данных"""
    connection = await get_db_connection()
    async with connection.cursor() as cursor:
        await cursor.execute('INSERT INTO users (user_id, username) VALUES (%s, %s)', (user_id, username))
        await connection.commit()
    connection.close()


async def get_user_settings(user_id):
    """Получение настроек пользователя"""
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT gif_length
                    FROM user_settings
                    WHERE user_id = %s;""",
                    (user_id,)
                )
                result = await cur.fetchone()
                if result:
                    return result[0]
                return None
    except Exception as e:
        logging.error(f"Ошибка при получении настроек для пользователя {user_id}: {e}")
        return None

async def save_user_settings(user_id, gif_length):
    """Сохранение настроек пользователя"""
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO user_settings (user_id, gif_length)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE gif_length = %s;
                    """,
                    (user_id, gif_length, gif_length)
                )
                await conn.commit()
                logging.info(f"Настройки для пользователя {user_id} обновлены. Длина GIF: {gif_length} секунд.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении настроек для пользователя {user_id}: {e}")