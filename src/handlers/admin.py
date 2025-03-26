from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from src.filters.admin import AdminFilter

admin_router = Router()

admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())

@admin_router.message(Command('admin'))
async def handle_admin(message: Message):
    await message.answer('Ты админ')
