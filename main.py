import asyncio
import logging
# from aiogram import F
from datetime import datetime
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
# from aiogram.enums import ParseMode
import os

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.getenv("BOT_TOKEN"))
# Диспетчер
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

# Хэндлер на команду /start

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text1 = "Привіт я був створений аби допомогти тобі кулінарними порадами"
    comands_text = "/dovidka - довідник\n/poshuk - пошук рецептів\n/myreceps - мої рецепти\n"
    text = f"Для продовжиння введи одну з команд на вибір\n{comands_text}"
    await message.answer(text1)
    await asyncio.sleep(1)
    await message.answer(text)


@dp.message(Command("dovidka"))
async def cmd_dovidka(message: types.Message):
    text1 = "Привіт ти потрапив до довідки тут ти зможеш отримати відповіді на сврої питання"
    comands_text = "/dovidka - довідник\n/poshuk - пошук рецептів\n/myreceps - мої рецепти\n"
    text = f"Для продовжиння введи одну з команд на вибір\n{comands_text}"
    await message.answer(text1)
    await asyncio.sleep(1)
    await message.answer(text)

    # await message.answer_dice(emoji="🎲", parse_mode=ParseMode.HTML)


@dp.message(Command("hello"))
async def cmd_hello(message: Message):
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message, started_at: datetime):
    await message.answer(f"bot Started at: {started_at}")
    await asyncio.sleep(1)
    await message.answer("Для отримання допомоги напишіть @ds0903")

    asyncio.run(main())


# ## НЕ ЧІПАЙ БО ПЕЗДА БУДЕ !!! ###
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# ## НЕ ЧІПАЙ БО ПЕЗДА БУДЕ !!! ###