from random import randint

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.for_facts import (
    get_facts_kb,
    get_science_inline_kb,
    get_historical_inline_kb,
)

from db.sqlite_db import get_facts, get_all_facts


class TypeFact(StatesGroup):
    choosing_type_fact = State()
    choosing_type_subfact = State()


router = Router()

fact_types = ["Факт дня", "Исторический факт", "Научный факт"]
science_subfacts = ["math", "bio", "space"]
historical_subfacts = ["old", "mid", "20th"]


@router.message(Command("get_facts"))
async def cmd_get_facts(message: Message, state: FSMContext):
    await message.answer(
        "Выбери какой факт вы хотите узнать: ", reply_markup=get_facts_kb()
    )
    await state.set_state(TypeFact.choosing_type_fact)


@router.message(TypeFact.choosing_type_fact, F.text.in_(fact_types))
async def choose_type_fact(message: Message, state: FSMContext):
    await state.update_data(choose_type_fact=message.text.lower())
    if message.text.lower() == "факт дня":
        facts = await get_all_facts()
        index = randint(0, len(facts)-1)
        await message.reply(facts[index][0], reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif message.text.lower() == "исторический факт":
        await message.reply("В какой области вы хотите исторический факт?",
                            reply_markup=get_historical_inline_kb())
        await state.set_state(TypeFact.choosing_type_subfact)
    elif message.text.lower() == "научный факт":
        await message.reply(
            "В какой области вы хотите научный факт?",
            reply_markup=get_science_inline_kb(),
        )
        await state.set_state(TypeFact.choosing_type_subfact)


@router.message(TypeFact.choosing_type_fact, F.text)
async def choose_type_fact_incorrect(message: Message):
    await message.answer(
        "Что-то пошло не так\n" "Воспользуйтесь кнопками!", reply_markup=get_facts_kb()
    )


@router.callback_query(TypeFact.choosing_type_subfact, F.data.in_(science_subfacts))
async def science_fact(callback: CallbackQuery, state: FSMContext):
    await state.update_data(choose_type_subfact=callback.data)
    if callback.data == "math":
        facts = await get_facts(fact_subtype="math")
        if len(facts) > 0:
            index = randint(0, len(facts) - 1)
            await callback.message.answer(text=facts[index][0],
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(text="Здесь еще нет фактов(",
                                          reply_markup=ReplyKeyboardRemove())
    elif callback.data == "bio":
        facts = await get_facts(fact_subtype="bio")
        if len(facts) > 0:
            index = randint(0, len(facts) - 1)
            await callback.message.answer(text=facts[index][0],
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(text="Здесь еще нет фактов(",
                                          reply_markup=ReplyKeyboardRemove())
    elif callback.data == "space":
        facts = await get_facts(fact_subtype="space")
        if len(facts) > 0:
            index = randint(0, len(facts) - 1)
            await callback.message.answer(text=facts[index][0],
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(text="Здесь еще нет фактов(",
                                          reply_markup=ReplyKeyboardRemove())

    await callback.answer()
    await state.clear()


@router.callback_query(TypeFact.choosing_type_subfact, F.data.in_(historical_subfacts))
async def historical_fact(callback: CallbackQuery, state: FSMContext):
    await state.update_data(choose_type_subfact=callback.data)
    if callback.data == "old":
        facts = await get_facts(fact_subtype="old")
        if len(facts) > 0:
            index = randint(0, len(facts) - 1)
            await callback.message.answer(text=facts[index][0],
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(text="Здесь еще нет фактов(",
                                          reply_markup=ReplyKeyboardRemove())
    elif callback.data == "mid":
        facts = await get_facts(fact_subtype="mid")
        if len(facts) > 0:
            index = randint(0, len(facts) - 1)
            await callback.message.answer(text=facts[index][0],
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(text="Здесь еще нет фактов(",
                                          reply_markup=ReplyKeyboardRemove())
    elif callback.data == "20th":
        facts = await get_facts(fact_subtype="20th")
        if len(facts) > 0:
            index = randint(0, len(facts) - 1)
            await callback.message.answer(text=facts[index][0],
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(text="Здесь еще нет фактов(",
                                          reply_markup=ReplyKeyboardRemove())

    await callback.answer()
    await state.clear()


@router.message(TypeFact.choosing_type_subfact, F.text)
async def choose_type_subfact_incorrect(message: Message):
    await message.answer(
        "Что-то пошло не так\n" "Воспользуйтесь инлайн-кнопками!", reply_markup=get_facts_kb()
    )
