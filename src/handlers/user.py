from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from src.filters.admin import AdminFilter

user_router = Router()

user_router.message.filter(AdminFilter())
user_router.callback_query.filter(AdminFilter())

@user_router.message(CommandStart())
async def handle_admin(message: Message):
    await message.answer('ку')
