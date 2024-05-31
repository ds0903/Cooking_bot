
import sqlite3


### Тут буде описана  логіка бази данних бота ###

# Операції з бд


async def search_recipe(recipe):
    conn = sqlite3.connect('bot_main.db')
    cursor = conn.cursor()
    for i in recipe:
        recipe_main = str(i)
    test = f"%{recipe_main}%"
    cursor.execute("SELECT * FROM food_main WHERE description LIKE ?", (test,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    if result:
        return result
    else:
        return "Помилка запиту"



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

    clas, description = data

    cursor.execute(
        "INSERT OR IGNORE INTO food_main (clas, description) VALUES (?, ?)", (clas, description)
    )
    # data = cursor.fetchone()

    if cursor.rowcount == 1:
        data = "Рецепт успішно додано"
    else:
        data = "Рецепт вже інсує"

    conn.commit()
    conn.close()

    return data


async def delete_data(id):
    conn = sqlite3.connect("bot_main.db")
    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM food_main WHERE id = ?", (id,)
    )

    if cursor.rowcount == 1:
        data = f"Рецепт №: {id} успішно видаленно"
    else:
        data = f"Рецепт №: {id} не існує"

    conn.commit()
    conn.close()

    return data


def get_all():
    conn = sqlite3.connect('bot_main.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food_main")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results