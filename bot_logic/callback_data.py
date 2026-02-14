from aiogram.filters.callback_data import CallbackData


class RoleSelect(CallbackData, prefix="role_select"):
    role: str
