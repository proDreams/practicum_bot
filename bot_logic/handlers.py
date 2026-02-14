from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot_logic.ai_roles import ROLES
from bot_logic.ai_tool import get_gigachat_response
from bot_logic.callback_data import RoleSelect

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


@handlers_router.callback_query(RoleSelect.filter())
async def ai_handler(
    query: CallbackQuery, callback_data: RoleSelect, state: FSMContext
):
    user_text = await state.get_value("user_text")

    ai_response = await get_gigachat_response(
        user_text=user_text, role=callback_data.role
    )

    await query.message.edit_text(text=ai_response, reply_markup=None)


@handlers_router.message()
async def role_handler(message: Message, state: FSMContext):
    await state.update_data(user_text=message.text)

    keyboard = [
        [
            InlineKeyboardButton(
                text=value.get("name"),
                callback_data=RoleSelect(role=key).pack(),
                style=value.get("style"),
            )
        ]
        for key, value in ROLES.items()
    ]

    await message.answer(
        text="В каком стиле хочешь получить ответ?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
