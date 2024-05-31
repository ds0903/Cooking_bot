import asyncio
# from aiogram import F
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.logic import search_recipe, search_recipe_by_clas, insert_data, delete_data, get_all
from aiogram.types import FSInputFile, KeyboardButton, ReplyKeyboardMarkup
router = Router()

### Тут знаходяться команди бота ###

about1 = None
# about2 = None

class Form(StatesGroup):
    food_class = State()
    poshuk_ingredient = State()
    my_receps = State()
    dodat = State()
    delete = State()
    dodat = State()
    description = State()

"""Логіка головного меню"""
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "Привіт я був створений аби допомогти тобі кулінарними порадами"
        )
    await message.answer(text)
    await asyncio.sleep(1)
    await cmd_menu(message)

@router.message(lambda message: message.text == 'Меню')
async def cmd_menu(message: types.Message):
    text1 = (
        "Виберіть потрібну вам дію"
        )

    # Создание кнопок для обычной клавиатуры
    kb = [
        [KeyboardButton(text="Довідник"), KeyboardButton(text="Пошук рецептів")],
        [KeyboardButton(text="Пошук рецептів за інгрідієнтами")],
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

@router.message(lambda message: message.text == 'Пошук рецептів')
async def cmd_poshuk(message: types.Message, state: FSMContext):
    """Організація пошуку рецептів"""

    kb = [
        [KeyboardButton(text="Супи")],[KeyboardButton(text="Напоі")],[KeyboardButton(text="Гриль")],
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer("Виберіть бажаний клас страв і бот поверне вам готові рецепти", reply_markup=keyboard)
    await state.set_state(Form.food_class)

    @router.message(lambda message: message.text == 'Супи', Form.food_class)
    async def cmd_sypi(message: types.Message):
        file_ids = []
        data = message.text
        response = await search_recipe_by_clas(data)
        for i in response:
            id, clas, about = i
            result = f"ID: {id}\nClass: {clas}\nDescription: {about}"
            await asyncio.sleep(1)
            await message.reply(result, reply_markup=types.ReplyKeyboardRemove())

            """Поки тестовий варіант відправки фоток"""
            if clas == "Супи":
                image_from_pc = FSInputFile("bot\handlers\photos\photo_2024-05-24_15-54-47.jpg")
                result = await message.answer_photo(
                    image_from_pc, caption="фотка 1"
                )
            #     file_ids.append(result.photo[-1].file_id)
            # if id == 2:
            #     image_from_pc = FSInputFile("bot\handlers\photos\photo_2024-05-24_15-54-47.jpg")
            #     result = await message.answer_photo(
            #         image_from_pc, caption="фотка 2"
            #     )
                file_ids.append(result.photo[-1].file_id)
        await state.clear()
        asyncio.sleep(6)
        await cmd_menu(message)

    @router.message(lambda message: message.text == 'Гриль', Form.food_class)
    async def cmd_grill(message: types.Message):
        data = message.text
        response = await search_recipe_by_clas(data)
        for i in response:
            id, clas, name, recipes, about = i
            result = f"ID: {id}\nClass: {clas}\nName: {name}\nRecipes: {recipes}\nDescription: {about}"
            await asyncio.sleep(1)
            await message.reply(result, reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        asyncio.sleep(6)
        await cmd_menu(message)


    @router.message(lambda message: message.text == 'Напоі', Form.food_class)
    async def cmd_napoi(message: types.Message):
        data = message.text
        response = await search_recipe_by_clas(data)
        for i in response:
            id, clas, name, recipes, about = i
            result = f"ID: {id}\nClass: {clas}\nName: {name}\nRecipes: {recipes}\nDescription: {about}"
            await asyncio.sleep(1)
            await message.reply(result, reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        asyncio.sleep(6)
        await cmd_menu(message)


@router.message(lambda message: message.text == 'Пошук рецептів за інгрідієнтами')
async def cmd_poshuk_ingredient(message: types.Message, state: FSMContext):

    await message.reply("Напишіть інгрідієнти для страви:\nНаприклад 'морква' або 'яловиЧИНА'", reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(Form.poshuk_ingredient)

    @router.message(Form.poshuk_ingredient)
    async def process_recipe_name(message: types.Message):

        recipe = message.text.split()

        recipe1 = await search_recipe(recipe)

        if recipe1:
            await message.answer(f"Рецепти які були знайдені за інгрідієнтами '{recipe}': знайдені.")
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


@router.message(lambda message: message.text == 'cmd_admin')
async def cmd_my_recipes(message: types.Message, state: FSMContext):
    # await state.set_state(Form.my_receps)

    kb = [
        [KeyboardButton(text="cmd_delete")], [KeyboardButton(text="cmd_dodat")],
        [KeyboardButton(text="Меню")], [KeyboardButton(text="cmd_all")],
    ]
    text = "Ти протрапив в секретне меню!"
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    @router.message(lambda message: message.text == 'cmd_dodat')
    async def cmd_dodat(message: types.Message, state: FSMContext):
        text = "Для додавання рецепту напишіть будьласка його клаc, назву рецепту, інгрідієнти, інформацію\n\nОбовьязково в тому порядку в якому наведено в прикладі!\n\n"
        text1 = "Наприклад: клас: 'Салати', назва: 'сільський', інгрідієнти: 'морква яловиЧИНА', опис: 'Опис рецепту'"
        await message.reply(f"{text}{text1}", reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(Form.dodat)

        @router.message(Form.dodat)
        async def process_register1(message: types.Message):
            global about1
            about1 = message.text
            await message.reply("Напишите опис рецепту 2")
            await state.clear()
            await state.set_state(Form.description)
        @router.message(Form.description)
        async def process_register2(message: types.Message):
            global about1
            # global about2
            about2 = message.text

            data_full = (about1, about2)
            about1 = None
            about2 = None

            response = await insert_data(data_full)
            # about2 = None
            await message.reply(response)
            await asyncio.sleep(2)
            await state.clear()
            await cmd_menu(message)


    @router.message(lambda message: message.text == 'cmd_delete')
    async def cmd_dodat(message: types.Message, state: FSMContext):
        text = "Для Видалення рецепту напишіть id рецепту(номер рецепту можна переглянути в меню всі рецепти)"
        await message.reply(f"{text}", reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(Form.delete)

        @router.message(Form.delete)
        async def process_register(message: types.Message):

            data = message.text
            response = await delete_data(data)
            await message.reply(response)
            await asyncio.sleep(2)
            await state.clear()
            await cmd_menu(message)

    @router.message(lambda message: message.text == 'cmd_all')
    async def cmd_all(message: types.Message, state: FSMContext):
        all = get_all()
        for result in all:
            await message.reply(f"{result}")


        # await message.reply(f"Вся інформація:{all}")
### Ідеї на майбутнє

# await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

# response1 = response[0]
#         id, clas, name, recipes, about = response1

#         result1 = f"ID: {id}\nClass: {clas}\nName: {name}\nRecipes: {recipes}\nDescription: {about}"
#         await message.reply(f"результат 1{result1}", reply_markup=types.ReplyKeyboardRemove())

#         await state.clear()

#         response2 = response[1]
#         id, clas, name, recipes, about = response2
#         result2 = f"ID: {id}\nClass: {clas}\nName: {name}\nRecipes: {recipes}\nDescription: {about}"
#         await message.answer(f"результат 2{result2}")

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