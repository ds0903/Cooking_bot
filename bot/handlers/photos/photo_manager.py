from aiogram import types
from aiogram.types import FSInputFile


async def photo_clas(message: types.Message, data):

    if "шо" in data.lower():
        image_from_pc = FSInputFile("bot\handlers\photos\photo_2024-05-24_15-54-47.jpg")
        await message.answer_photo(image_from_pc, caption="Борщ")



# Хочеш відправити фото копіюї else і шлях до фото наприклад

# elif "fff" in data.lower():
#     image_from_pc = FSInputFile("Шлях до фото")
#     await message.answer_photo(
#         image_from_pc, caption="Підпис під фотографією"
# І так до безкінечності

"""Приклад відправик фоток"""
# file_ids = []
# if id == 2:
#     image_from_pc = FSInputFile("bot\handlers\photos\photo_2024-05-24_15-54-47.jpg")
#     result = await message.answer_photo(
#         image_from_pc, caption="фотка 2"
#     )
# file_ids.append(result.photo[-1].file_id)
