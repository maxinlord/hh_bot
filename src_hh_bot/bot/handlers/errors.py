from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, ErrorEvent
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
from tools import get_text_message
from bot.keyboards import k_start_menu, k_types_of_reg, k_back



router = Router()

@router.error()
async def error_handler(event: ErrorEvent):
    print(event.exception)