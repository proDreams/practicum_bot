from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot_logic.ai_tool import get_gigachat_response

handlers_router = Router()


@handlers_router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer(
        text="""
    Привет!
    
Я бот для важных переговоров! 

Просто отправь мне свой текст...
    """
    )


@handlers_router.message()
async def ai_handler(message: Message):
    ai_response = await get_gigachat_response(user_text=message.text)

    await message.answer(text=ai_response)
