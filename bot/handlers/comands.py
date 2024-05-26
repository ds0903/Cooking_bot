import asyncio
from aiogram import F
# from datetime import datetime
from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
from handlers.logic import sqlite3
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
router = Router()

### Тут знаходяться команди бота ###


"""Тут описані всі команди"""

@router.message(lambda message: message.text == 'Меню')
async def cmd_start(message: types.Message):
    text1 = (
        "Виберіть потрібну вам кнопку"
        )
    
    # Создание кнопок для обычной клавиатуры
    kb = [
        [KeyboardButton(text="Довідник"), KeyboardButton(text="Пошук рецептів")],
        [KeyboardButton(text="Пошук рецептів за інгрідієнтами"), KeyboardButton(text="Мої рецепти")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await asyncio.sleep(1)
    await message.answer(text1, reply_markup=keyboard)

@router.message(lambda message: message.text == 'Довідник')
async def process_with_puree(message: types.Message):
    """Тут розписана всяка херня буде"""
    text1 = "1.кнопка в меню це сам довідник\n2.пошук рецептів\n3.пошук рецептів за інгрідієнтами\n4.мої рецепти"
    text2 = "Для отримання допомоги напишіть адміну @ds0903"
    kb = [
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text1)
    await asyncio.sleep(2)
    await message.answer(text2, reply_markup=keyboard)


async def search_recipe(recipe_name):
    """Запрос к базе по поиску рецептов"""
    conn = sqlite3.connect('bot_main.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE name = ?", (recipe_name,))
    recipe = cursor.fetchone()

    cursor.close()
    conn.close()

    return recipe


"""Логіка головного меню"""
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "Привіт я був створений аби допомогти тобі кулінарними порадами"
        )
    text1 = (
        "Для проводовження перейди в меню"
        )

    kb = [
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(text)
    await asyncio.sleep(1)
    await message.answer(text1, reply_markup=keyboard)


@router.message(lambda message: message.text == 'Пошук рецептів')
async def cmd_poshuk(message: types.Message):
    """Організація пошуку рецептів"""

    kb = [
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    # await asyncio.sleep(1)
    await message.reply("Напишіть клас страви:\nНаприклад 'Салат' або 'коктелі'", reply_markup=types.ReplyKeyboardRemove())
    # await message.answer("Напишіть клас страви:\nНаприклад 'Салат' або 'коктелі'")
    await asyncio.sleep(2)
    await message.answer("Для повернення в головне меню натисніть кнопку 'Меню'", reply_markup=keyboard)

    @router.message()
    async def process_recipe_name(message: types.Message):
        """Обработка введенного пользователем имени рецепта"""

        recipe_name = message.text
        recipe = await search_recipe(recipe_name)

        if recipe:
            await message.answer(f"Рецептів за назвою '{recipe_name}': знайдені.")
        else:
            await message.answer(f"Рецептів за назвою '{recipe_name}' не знайдені.")


@router.message(lambda message: message.text == 'Пошук рецептів за інгрідієнтами')
async def cmd_poshuk_ingreee(message: types.Message):
    """Організація пошуку рецептів за інгрідієнтами"""

    kb = [
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply("Напишіть інгрідієнти для страви:\nНаприклад 'морква' або 'яловиЧИНА'", reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await message.answer("Для повернення в головне меню натисніть кнопку 'Меню'", reply_markup=keyboard)

    @router.message()
    async def process_recipe_name(message: types.Message):
        """Обработка введенного пользователем имени рецепта"""

        recipe_name = message.text
        recipe = await search_recipe(recipe_name)

        if recipe:
            await message.answer(f"Рецептів за інгрідієнтами '{recipe_name}': знайдені.")
        else:
            await message.answer(f"Рецептів за інгрідієнтами '{recipe_name}' не знайдено.")


@router.message(lambda message: message.text == 'Мої рецепти')
async def cmd_my_recipes(message: types.Message):
    """Організація пошуку рецептів за інгрідієнтами"""

    kb_menu = [
        [KeyboardButton(text="Меню")],
    ]

    # kb = [
    #     [KeyboardButton(text="Видалити"), KeyboardButton(text="Відредагувати")],
    #     [KeyboardButton(text="Додати"), KeyboardButton(text="Мої рецепти")],
    # ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_menu, resize_keyboard=True)
    await message.reply("Напишіть інгрідієнти для страви:\nНаприклад 'морква' або 'яловиЧИНА'", reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await message.answer("Для повернення в головне меню натисніть кнопку 'Меню'", reply_markup=keyboard)

    @router.message()
    async def process_recipe_name(message: types.Message):
        """Обработка введенного пользователем имени рецепта"""

        recipe_name = message.text
        recipe = await search_recipe(recipe_name)

        if recipe:
            await message.answer(f"Рецептів за інгрідієнтами '{recipe_name}': знайдені.")
        else:
            await message.answer(f"Рецептів за інгрідієнтами '{recipe_name}' не знайдено.")


### Ідеї на майбутнє

# await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

# @router.message(Command("poshuk"))
# async def cmd_poshuk(message: types.Message):
#     """Виконуватиметься наш пошук рецептів за назвами"""

#     content = Text(
#         "Шановний, ",
#         Bold(message.from_user.full_name),
#         "введіть потрібний вам рецепт"
#     )
#     await message.answer(
#         **content.as_kwargs()
#     )

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


# @router.message(F.text.lower() == "test")
# async def cmd_hi(message: types.Message):

#     await message.answer("/dovidka")
#     await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())