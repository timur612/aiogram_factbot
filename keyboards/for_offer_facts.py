from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def offer_facts_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Предложить факт"),
        KeyboardButton(text="Посмотреть предложенные")
    )
    return builder.as_markup(
        resize_keyboard=True
    )


def get_offer_facts_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Исторический факт"),
        KeyboardButton(text="Научный факт"),
    )
    return builder.as_markup(
        resize_keyboard=True, input_field_placeholder="Выберите интересующий факт"
    )


def get_offers_list(offers: list) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for offer in offers:
        builder.row(
            KeyboardButton(text=offer[1] + "_" + str(offer[0]) + "_" + offer[2] + "_" + offer[3])
        )
    return builder.as_markup(
        resize_keyboard=True
    )
