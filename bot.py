import asyncio
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

feedback_users = {}

# ---------- Клавіатури ----------
start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="⚛️ PvP")]],
    resize_keyboard=True
)

main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🧠 Що ми робимо")],
        [types.KeyboardButton(text="🧪 Де використовується")],
        [types.KeyboardButton(text="👥 Для кого")],
        [types.KeyboardButton(text="📩 Зв’язатися з нами")],
        [types.KeyboardButton(text="💬 Залишити фідбек")]
    ],
    resize_keyboard=True
)

back_to_menu = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="🏠 Головне меню")]],
    resize_keyboard=True
)

# ---------- /start ----------
@router.message(CommandStart())
async def start(message: types.Message):
    user = message.from_user
    print(f"НОВИЙ КОРИСТУВАЧ → ID:{user.id}, @{user.username}, {user.first_name}")

    await message.answer(
        "🎮 *Ми — команда PvP, або портал в пекло.*\n\n"
        "Натисни кнопку нижче, щоб дізнатися більше 👇",
        parse_mode="Markdown",
        reply_markup=start_keyboard
    )

# ---------- PvP ----------
@router.message(F.text == "⚛️ ATLANT 3D")
async def open_menu(message: types.Message):
    await message.answer("Головне меню:", reply_markup=main_menu)

# ---------- Меню ----------
@router.message(F.text == "🧠 Що ми робимо")
async def what_we_do(message: types.Message):
    await message.answer(
        "PvP — deep tech стартап, що створює технологію атомного друку "
        "для мікро- та наноструктур.",
        reply_markup=back_to_menu
    )

@router.message(F.text == "🧪 Де використовується")
async def where_used(message: types.Message):
    await message.answer(
        "• сенсори\n"
        "• мікроелектроніка\n"
        "• фотоніка\n"
        "• космічні технології",
        reply_markup=back_to_menu
    )

@router.message(F.text == "👥 Для кого")
async def for_whom(message: types.Message):
    await message.answer(
        "• інженери\n"
        "• R&D команди\n"
        "• стартапи\n"
        "• університети",
        reply_markup=back_to_menu
    )

@router.message(F.text == "📩 Зв’язатися з нами")
async def contact(message: types.Message):
    await message.answer(
        "Telegram контакти:\n"
        "• @duu_sk (Founder)\n"
        "• @palenuch (CO-Founder)",
        reply_markup=back_to_menu
    )

# ---------- Фідбек (БЕЗ ЗБЕРЕЖЕННЯ) ----------
@router.message(F.text == "💬 Залишити фідбек")
async def ask_feedback(message: types.Message):
    feedback_users[message.from_user.id] = True
    await message.answer("Напиши свій фідбек 👇")

@router.message()
async def handle_all(message: types.Message):
    user_id = message.from_user.id

    if message.text == "🏠 Головне меню":
        await message.answer("Головне меню:", reply_markup=main_menu)
        return

    if feedback_users.get(user_id):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] FEEDBACK → {message.from_user.id}: {message.text}")

        feedback_users.pop(user_id)
        await message.answer("Дякуємо за фідбек ❤️", reply_markup=main_menu)

# ---------- Запуск ----------
async def main():
    print("БОТ ЗАПУСТИВСЯ")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
