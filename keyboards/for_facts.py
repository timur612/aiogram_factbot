from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_facts_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Факт дня"),
        KeyboardButton(text="Исторический факт"),
        KeyboardButton(text="Научный факт"),
    )
    return builder.as_markup(
        resize_keyboard=True, input_field_placeholder="Выберите интересующий факт"
    )


def get_science_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Математика", callback_data="math"),
        InlineKeyboardButton(text="Биология", callback_data="bio"),
        InlineKeyboardButton(text="Космос", callback_data="space"),
    )

    return builder.as_markup()


def get_historical_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Древние века", callback_data="old"),
        InlineKeyboardButton(text="Средние века", callback_data="mid"),
        InlineKeyboardButton(text="20 век", callback_data="20th"),
    )

    return builder.as_markup()


def get_cancel_btn() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Закончить")
    )
    return builder.as_markup(resize_keyboard=True)
