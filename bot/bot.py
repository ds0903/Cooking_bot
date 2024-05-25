import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import comands
import os


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.getenv("BOT_TOKEN"))
# Диспетчер
dp = Dispatcher()
# Змінна що відповідає за таймер потім розповім
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

# Включаємо роутер
dp.include_router(comands.router)








# ## НЕ ЧІПАЙ бо буде торба !!! ###
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# ## НЕ ЧІПАЙ бо буде торба !!! ###
