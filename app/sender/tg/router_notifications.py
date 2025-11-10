from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command


router_notifications = Router(name="notifications")


@router_notifications.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text="Notifications on")


@router_notifications.message(Command("off"))
async def cmd_of(message: Message):
    await message.answer(text=f"Notifications off")
