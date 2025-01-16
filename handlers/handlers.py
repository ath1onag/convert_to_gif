import os
from aiogram import Bot, Router, F
from aiogram.filters import Command
from database.database import create_database, insert_database
from aiogram import types
from aiogram.types.input_file import FSInputFile
from moviepy import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config_data.config import UPLOAD_PATH, Config, load_config
from keyboard import buttons as kb
from lexicon.lexicon import LEXICON_RU
import logging

config: Config = load_config()

bot = Bot(token=config.tg_bot.token)

class File(StatesGroup):
    file = State()
logging.basicConfig(level=logging.INFO)
router = Router()
@router.message(Command(commands=['start']))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    await insert_database(user_id, username)
    keyboard = kb.main_menu

    await message.answer(LEXICON_RU['/start'], reply_markup=keyboard)

@router.message(Command(commands=['help']))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(LEXICON_RU['/help'])

@router.message(F.text =='Помощь')
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(LEXICON_RU['/help'])

@router.message(F.text =='Конвертировать видео в GIF')
async def get_video(message: types.Message, state: FSMContext):
    await state.set_state(File.file)
    await message.answer('Выгрузите Ваш файл.')
@router.message(File.file)
async def handle_video(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        # Проверка наличия директории для загрузки
        if not os.path.exists(UPLOAD_PATH):
            os.makedirs(UPLOAD_PATH)

        if not message.video:
            await message.reply("Ошибка: Пожалуйста, отправьте видеофайл.")
            return
        video = message.video
        file_id = video.file_id
        await state.update_data(file=file_id)
        await message.reply("Обрабатываю запрос...")
        data = await state.get_data()
        file = data.get("file")
        file = await bot.get_file(file_id)

        # Скачиваем видеофайл
        video_path = f"{UPLOAD_PATH}{video.file_id}.mp4"
        await bot.download_file(file.file_path, video_path)


        # Конвертация в GIF
        gif_path = os.path.splitext(video_path)[0] + ".gif"

        # Обрезка видео по длительности и создание GIF
        clip = VideoFileClip(video_path)
        clip.write_gif(gif_path, fps=5)  # Можно увеличить fps для лучшего качества

        document = FSInputFile(f"{UPLOAD_PATH}{video.file_id}.gif")
        await bot.send_document(user_id, document, caption=f'Ваш GIF-файл!')

    except Exception as e:
        # Отправка сообщения об ошибке с подробным описанием
        await message.reply(f"Ошибка при обработке видео: {str(e)}")

    await state.clear()
