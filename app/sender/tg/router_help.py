from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command


# TODO: router -> в отдельного бота техподдержки
router_help = Router(name="help")


@router_help.message(Command("error"))
async def cmd_start(message: Message):
    await message.answer(text="Message about error saved")
