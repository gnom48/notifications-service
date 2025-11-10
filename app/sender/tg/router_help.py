from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command


router_help = Router("help")  # TODO: router -> в отдельного бота техподдержки


@router_help.message(Command("error"))
async def cmd_start(message: Message):
    await message.answer(text="Message about error saved")
