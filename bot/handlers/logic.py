
import sqlite3


### Тут буде описана  логіка бази данних бота ###

# Операції з бд


async def search_recipe(recipe_name):
    conn = sqlite3.connect('bot_main.db')
    cursor = conn.cursor()
    test1, test2 = recipe_name
    test = f"{test1} {test2}"
    for recipe in recipe_name:

        cursor.execute("SELECT * FROM food_main WHERE recipes = ?", (test,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result


async def search_recipe_by_clas(clas):
    conn = sqlite3.connect('bot_main.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food_main WHERE clas = ?", (clas,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    if results:
        return results
    else:
        return None,None,None,None,None


async def insert_data(data):
    conn = sqlite3.connect("bot_main.db")
    cursor = conn.cursor()

    clas, name, recipes, description = data

    cursor.execute(
        "INSERT OR IGNORE INTO food_my (clas, name, recipes, description) VALUES (?, ?, ?, ?)", (clas, name, recipes, description)
    )
    # data = cursor.fetchone()

    if cursor.rowcount == 1:
        data = "Рецепт успішно додано"
    else:
        data = "Рецепт вже інсує"

    conn.commit()
    conn.close()

    return data
