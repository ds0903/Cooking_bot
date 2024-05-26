import asyncio
# from aiogram import F

import sqlite3


### Тут буде описана  логіка бази данних бота ###

# Операції з бд


async def search_recipe(recipe_name):
    """Запрос к базе по поиску рецептов"""
    conn = sqlite3.connect('bot_main.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE name = ?", (recipe_name,))
    recipe = cursor.fetchone()

    cursor.close()
    conn.close()

    return recipe
