from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from db.sqlite_db import create_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await create_user(str(message.from_user.id), 0)
    await message.answer(
        "Привет! Я бот фактов\n"
        "Напишите (/get_facts), если хотите узнать интересный факт\n"
        "Напшите (/offer_facts), если хотите добавить интересный факт",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(text="Нечего отменять", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
