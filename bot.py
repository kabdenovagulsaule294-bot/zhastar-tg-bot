"""Информационный бот МРЦ. Python 3.12, aiogram 3.x."""
import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

# Редактируемые формулировки по материалам МРЦ, не дословный текст сайта.
ABOUT = (
    "О нас\n\n"
    "Молодёжный ресурсный центр — пространство возможностей для молодёжи. "
    "Мы помогаем молодым людям раскрывать способности, получать полезный опыт, "
    "участвовать в общественной жизни и реализовывать свои идеи.\n\n"
    "Здесь можно узнать о молодёжных проектах, волонтёрстве, "
    "профориентации и возможностях занятости."
)
DIRECTIONS = (
    "Направления\n\n"
    "• Волонтёрство — участие в добрых делах и помощь окружающим.\n"
    "• Молодёжные проекты — развитие инициатив и реализация идей.\n"
    "• Профориентация — знакомство с профессиями, встречи и консультации.\n"
    "• Практика и стажировки — получение опыта и полезных навыков.\n"
    "• Временная занятость — информация о возможностях работы.\n\n"
    "Уточнить условия участия можно по телефону центра в разделе «Контакты»."
)
CONTACTS = (
    "Контакты\n\n"
    "Молодёжный ресурсный центр\n"
    "Адрес: ул. Мелехова, 52\n"
    "Телефон: 8 705 375 9414"
)

MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О нас"), KeyboardButton(text="Направления")],
        [KeyboardButton(text="Контакты")],
    ],
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Выберите раздел",
)
router = Router()
router.message.filter(F.chat.type == "private")


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Добро пожаловать в бот Молодёжного ресурсного центра!\n"
        "Узнайте о нас, направлениях работы и способах связи.\n\n"
        "Выберите раздел с помощью кнопок ниже 👇",
        reply_markup=MENU,
    )


@router.message(F.text == "О нас")
async def about(message: Message) -> None:
    await message.answer(ABOUT, reply_markup=MENU)


@router.message(F.text == "Направления")
async def directions(message: Message) -> None:
    await message.answer(DIRECTIONS, reply_markup=MENU)


@router.message(F.text == "Контакты")
async def contacts(message: Message) -> None:
    await message.answer(CONTACTS, reply_markup=MENU)


@router.message()
async def fallback(message: Message) -> None:
    await message.answer("Пожалуйста, выберите раздел на клавиатуре ниже.", reply_markup=MENU)


async def main() -> None:
    token = "8868788199:AAEc609KJfk7_XSDJtAmyxmaCMPReZuOkZc"
    if not token:
        raise SystemExit("Задайте переменную окружения BOT_TOKEN перед запуском.")
    dp = Dispatcher()
    dp.include_router(router)
    async with Bot(token=token) as bot:
        # Переключаем бота на polling, сохраняя ожидающие сообщения.
        await bot.delete_webhook(drop_pending_updates=False)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            close_bot_session=False,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
