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
    token ="8868788199:AAEc609KJfk7_XSDJtAmyxmaCMPReZuOkZc"
    if not token or token == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise SystemExit("Укажите BOT_TOKEN в файле .env рядом с bot.py или в окружении.")
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
