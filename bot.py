import config
import logging
from siteparser import Parsercity

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from sqlighter import SQLcity

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
db = SQLcity("db.db")

# Активация подписки
@dp.message_handler(commands=["subscribe"])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)

    await message.answer("Вы успешно подписались на парсинг бота!")


# Отписка
@dp.message_handler(commands=["unsubscribe"])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны!")
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны")


# меню парсинга
@dp.message_handler(commands=["start"])
async def subscribe(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Парсим в базу")
    keyboard.add(button_1)
    text = "Давайте спарсим городские населенные пункты Мос.области в базу"
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(Text(equals="Парсим в базу"))
async def parse_citues(message: types.Message):
    Parsercity(config.PARSE_URL).add_in_db(db)
    await message.reply(
            "Парсинг прошел успешно, введите название населенного пункта"
        )


# Проверка текста сообщения, отправка города
@dp.message_handler()
async def find_city(message: types.Message):
    if len(db.get_city_names(message.text[:10])) > 1:
        print(message.text[:10])
        text = db.get_city_names_str(message.text[:10])
        text += "\nНашел несколько городов, уточните запрос"
        await message.answer(text, parse_mode="MarkdownV2")
    elif len(db.get_city_names(message.text[:10])) == 0:
        text = "Что то не могу найти города в базе по вашему запросу, попробуйте набрать другие буквы"
        await message.answer(text)
    else:
        text = db.get_city_url()
        text += db.get_city_population()
        await message.answer(text, parse_mode="HTML")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
