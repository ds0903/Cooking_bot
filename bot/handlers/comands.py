import asyncio

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from handlers.logic import (delete_data, get_all, insert_data, search_recipe,
                            search_recipe_by_clas)
from handlers.photos.photo_manager import photo_clas

router = Router()

### Тут знаходяться команди бота ###


class Form(StatesGroup):
    food_class = State()
    poshuk_ingredient = State()
    my_receps = State()
    dodat = State()
    delete = State()
    description = State()


"""Логіка головного меню"""


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = "Привіт я був створений аби допомогти тобі кулінарними порадами"
    await message.answer(text)
    await asyncio.sleep(1)
    await cmd_menu(message)


@router.message(lambda message: message.text == "Меню")
async def cmd_menu(message: types.Message):
    text1 = "Виберіть потрібну вам дію"

    # Создание кнопок для обычной клавиатуры
    kb = [
        [KeyboardButton(text="Довідник"), KeyboardButton(text="Пошук рецептів")],
        [KeyboardButton(text="Пошук рецептів за інгрідієнтами")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await asyncio.sleep(1)
    await message.answer(text1, reply_markup=keyboard)


@router.message(lambda message: message.text == "Довідник")
async def process_with_puree(message: types.Message):
    """Тут розписана всяка херня буде"""
    text1 = "1.кнопка в меню це сам довідник\n2.пошук рецептів\n3.пошук рецептів за інгрідієнтами"
    text2 = "Для отримання допомоги напишіть адміну @ds0903"
    kb = [
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text1)
    await asyncio.sleep(2)
    await message.answer("👨‍💻")
    await asyncio.sleep(0.25)
    await message.answer(text2, reply_markup=keyboard)


@router.message(lambda message: message.text == "Пошук рецептів")
async def cmd_poshuk(message: types.Message, state: FSMContext):
    """Організація пошуку рецептів"""

    kb = [
        [KeyboardButton(text="Супи")],
        [KeyboardButton(text="деСЕРТИ")],
        [KeyboardButton(text="Гриль")],
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(
        "Виберіть бажаний клас страв і бот поверне вам готові рецепти",
        reply_markup=keyboard,
    )
    await state.set_state(Form.food_class)

# Шаблон для рецептів

    @router.message(lambda message: message.text == "Супи", Form.food_class)
    async def cmd_sypi(message: types.Message):
        data = message.text
        response = await search_recipe_by_clas(data)
        for i in response:                                          # Шаблон для рецептів
            id, clas, about = i
            result = f"ID: {id}\nClass: {clas}\nDescription: {about}"
            await asyncio.sleep(1)
            await message.reply(result, reply_markup=types.ReplyKeyboardRemove())
            await photo_clas(message, about)

        await state.clear()
        await asyncio.sleep(3)
        await cmd_menu(message)

# Шаблон для рецептів
    @router.message(lambda message: message.text == "Гриль", Form.food_class)
    async def cmd_grill(message: types.Message):
        data = message.text
        response = await search_recipe_by_clas(data)
        for i in response:
            id, clas, about = i
            result = f"ID: {id}\nClass: {clas}\nDescription: {about}"
            await asyncio.sleep(1)
            await message.reply(result, reply_markup=types.ReplyKeyboardRemove())
            await photo_clas(message, about)

        await state.clear()
        await asyncio.sleep(3)
        await cmd_menu(message)

    @router.message(lambda message: message.text == "деСЕРти", Form.food_class)
    async def cmd_napoi(message: types.Message):
        data = message.text
        response = await search_recipe_by_clas(data)
        for i in response:
            id, clas, about = i
            result = f"ID: {id}\nClass: {clas}\nDescription: {about}"
            await asyncio.sleep(1)
            await message.reply(result, reply_markup=types.ReplyKeyboardRemove())
            await photo_clas(message, about)

        await state.clear()
        await asyncio.sleep(3)
        await cmd_menu(message)


@router.message(lambda message: message.text == "Пошук рецептів за інгрідієнтами")
async def cmd_poshuk_ingredient(message: types.Message, state: FSMContext):

    await message.reply(
        "Напишіть інгрідієнти для страви:\nНаприклад 'морква' або 'яловиЧИНА'",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    await state.set_state(Form.poshuk_ingredient)


@router.message(Form.poshuk_ingredient)
async def process_recipe_name(message: types.Message, state: FSMContext):

    recipe = message.text.split()

    recipe1 = await search_recipe(recipe)

    if recipe1 != "Помилка запиту":
        await message.answer(
            f"Рецепти які були знайдені за інгрідієнтами '{recipe}': знайдені."
        )
        for i in recipe1:
            await asyncio.sleep(1)
            await message.answer(f"Репецт: {i}")
        await state.clear()
        await asyncio.sleep(1)
        await cmd_menu(message)
    else:
        await message.answer(f"Рецептів за інгрідієнтами '{recipe}' не знайдено.")
        await state.clear()
        await asyncio.sleep(1)
        await cmd_menu(message)


@router.message(lambda message: message.text == "cmd_admin")
async def cmd_admin(message: types.Message, state: FSMContext):
    # await state.set_state(Form.my_receps)

    kb = [
        [KeyboardButton(text="cmd_delete")],
        [KeyboardButton(text="cmd_dodat")],
        [KeyboardButton(text="cmd_all")],
        [KeyboardButton(text="Меню")],
    ]
    text = "Ти протрапив в секретне меню!\nТут ти можеш додати/видалити та отримати всі рецепти"
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    @router.message(lambda message: message.text == "cmd_dodat")
    async def cmd_dodat(message: types.Message, state: FSMContext):
        text = "Для додавання рецепту напишіть будьласка спочатку його клаc."
        text1 = "З доступних є лиш 3 класи.\nСупи\nГриль\nдеСЕРТИ"
        await message.reply(f"{text}", reply_markup=types.ReplyKeyboardRemove())
        await asyncio.sleep(1)
        await message.answer(f"{text1}")
        await state.set_state(Form.dodat)

        @router.message(Form.dodat)
        async def process_register1(message: types.Message, state: FSMContext):
            about1 = message.text
            if about1 == "Супи" or message.text == "Гриль" or message.text == "деСЕРТИ":
                await state.update_data(about1=about1)
                await message.reply(
                    f"Напишіть тепер опис рецепту\nНаприклад: Суп солянка з морквой"
                )
                await state.set_state(Form.description)
            else:
                await message.answer(
                    f"Такого Клаасу рецепту не існує!\n\n{text1}\n\nВводь заново тепер cmd_dodat"
                )
                await state.clear()

        @router.message(Form.description)
        async def process_register2(message: types.Message, state: FSMContext):

            about2 = message.text
            user_data = await state.get_data()
            about1 = user_data["about1"]
            data_full = (about1, about2)

            response = await insert_data(data_full)

            await message.reply(response)
            await asyncio.sleep(2)
            await state.clear()
            await cmd_admin(message, state)

    @router.message(lambda message: message.text == "cmd_delete")
    async def cmd_delete(message: types.Message, state: FSMContext):
        text = "Для Видалення рецепту напишіть id рецепту\nP.S.(номер рецепту можна переглянути в меню всі рецепти)"
        await message.reply(f"{text}", reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(Form.delete)

        @router.message(Form.delete)
        async def process_register(message: types.Message):

            data = message.text
            response = await delete_data(data)
            await message.reply(response)
            await state.clear()
            await asyncio.sleep(2)
            await cmd_admin(message, state)

    @router.message(lambda message: message.text == "cmd_all")
    async def cmd_all(message: types.Message, state: FSMContext):
        all = get_all()
        for result in all:
            await message.reply(f"{result}")
            await asyncio.sleep(1)
            if result == all[-1]:
                await message.reply("Це була вся інформація")
                await asyncio.sleep(1)
                await cmd_admin(message, state)


### Ідеї на майбутнє

# приклад як можна вставляти емодзі
# мажано лишати легку затримку аби сильно не різало очі
#     await message.answer("👨‍💻")
#     await asyncio.sleep(0.25)
# Видалення клавіатури
# await message.reply("test", reply_markup=types.ReplyKeyboardRemove())