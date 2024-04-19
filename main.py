import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import requests

# Ваш API ключ от Telegram
BOT_TOKEN = '7133328183:AAEbno9akd-k7WxQdK9k2uNomi5DYzlCrC0'

# Ваш API ключ от Instagram
INSTAGRAM_TOKEN = 'IGQWROLU1ha2oybEJ3Nnl2Qkxfb2hKZA2IxenB1Y3ZAyYWVka3F0eElWUmNZAMElJejd0MnV5ZA1BiTXQ5YXBaS2JtTFNOOHlzLWFiemdSWVFSM3lveldoX18zUE8tWThiZAUNLM0UtYU5IOThPZAHJIVjFCQ2E2RlJjWlEZD'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    search_button = types.InlineKeyboardButton(text="Поиск в Instagram", callback_data="search")
    keyboard.add(search_button)
    await message.answer("Привет! Я бот для поиска в Instagram. Нажми кнопку ниже, чтобы начать поиск.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'search')
async def process_search(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите ваш запрос для поиска в Instagram:")


@dp.message_handler()
async def search_in_instagram(message: types.Message):
    query = message.text

    # Выполняем запрос к Instagram API
    instagram_url = f'https://api.instagram.com/v1/users/self/media/recent/?access_token={INSTAGRAM_TOKEN}&q={query}'
    response = requests.get(instagram_url, verify=False)

    if response.status_code == 200:
        # Если запрос успешен, отправляем пользователю результат
        result = response.json()
        for post in result['data']:
            caption = post.get('caption', 'No caption available')
            photos = [photo['url'] for photo in post.get('images', [])]
            for photo in photos:
                await message.answer_photo(photo, caption=caption)
    else:
        await message.answer("Произошла ошибка при выполнении запроса к Instagram")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
