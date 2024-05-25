import asyncio
# from aiogram import F
from datetime import datetime
from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text1 = "Привіт я був створений аби допомогти тобі кулінарними порадами"
    comands_text = "/dovidka - довідник\n/poshuk - пошук рецептів\n/myreceps - мої рецепти\n/poshuk_receps - пошук рецептів за інгрідієнтами"
    text = f"Для продовжиння введи одну з команд на вибір\n{comands_text}"
    await message.answer(text1)
    await asyncio.sleep(1)
    await message.answer(text)

"""Тут описані всі команди"""

@router.message(Command("dovidka"))
async def cmd_dovidka(message: types.Message):
    """Тут розписана всяка херня буде"""

    text1 = "Привіт ти потрапив до довідки тут ти зможеш отримати відповіді на сврої питання"
    comands_text = "/dovidka - довідник\n/poshuk - пошук рецептів\n/myreceps - мої рецепти\n"
    text = f"Для продовжиння введи одну з команд на вибір\n{comands_text}"
    await message.answer(text1)
    await asyncio.sleep(1)
    await message.answer(text)

@router.message(Command("poshuk"))
async def cmd_poshuk(message: types.Message):
    """Виконуватиметься наш пошук рецептів за назвами"""

    content = Text(
        "Шановний, ",
        Bold(message.from_user.full_name),
        "введіть потрібний вам рецепт"
    )
    await message.answer(
        **content.as_kwargs()
    )

@router.message(Command("poshuk_receps"))
async def cmd_receps(message: types.Message):
    """Бот отримуватиме данні від користувача і після видаватиме рецепти за інгрідієнтами"""

    text = "Будь лакска напишіть через пробіл інгрідієнти для пошуку рецептів"
    await message.answer(text)
    await asyncio.sleep(1)
    await message.answer("Натисніть /help для допомоги")

@router.message(Command("myreceps"))
async def cmd_myreceps(message: types.Message):
    """Бот отримуватиме данні від користувача і після видаватиме рецепти за його профілем"""

    text = "тут будуть збережені ваші рецепти"
    await message.answer(text)
    await asyncio.sleep(1)
    await message.answer("Натисніть /help для допомоги")

@router.message(Command("help"))
async def cmd_help(message: types.Message, started_at: datetime):
    """Тут наша допомога"""

    await message.answer("Для отримання допомоги напишіть @ds0903")



### Ідеї на майбутнє
# @router.message(Command("hello"))
# async def cmd_hello(message: Message):
#     content = Text(
#         "Hello, ",
#         Bold(message.from_user.full_name)
#     )
#     await message.answer(
#         **content.as_kwargs()
#     )

    # await message.answer_dice(emoji="🎲", parse_mode=ParseMode.HTML)