from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))


# Настройки для MySQL
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'telegram_db'
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'password'

UPLOAD_PATH = './uploads/'