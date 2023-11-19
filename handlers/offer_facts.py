from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.for_offer_facts import offer_facts_kb, get_offer_facts_kb, \
    get_offers_list
from keyboards.for_facts import get_science_inline_kb, \
    get_historical_inline_kb

from db.sqlite_db import create_offer_fact, is_user_admin, get_offer_facts, \
    delete_offer_fact, create_fact


class OfferFact(StatesGroup):
    choosing_get_offer = State()
    choosing_type_offer = State()
    choosing_subtype_offer = State()
    create_offer = State()
    get_offer = State()


router = Router()

fact_types = ["Факт дня", "Исторический факт", "Научный факт"]
science_subfacts = ["math", "bio", "space"]
historical_subfacts = ["old", "mid", "20th"]


@router.message(Command("offer_facts"))
async def cmd_offer_facts(message: Message, state: FSMContext):
    if await is_user_admin(str(message.from_user.id)):
        await message.reply(text="Что вы хотите сделать?",
                            reply_markup=offer_facts_kb())
        await state.set_state(OfferFact.choosing_get_offer)
    else:
        await message.reply(text="Для продолжения выберете тип факта",
                            reply_markup=get_offer_facts_kb())
        await state.set_state(OfferFact.choosing_type_offer)


@router.message(OfferFact.choosing_get_offer,
                F.text.in_(['Предложить факт', 'Посмотреть предложенные']))
async def choose_for_admin(message: Message, state: FSMContext):
    if message.text.lower() == "предложить факт":
        await message.answer(text="Для продолжения выберете тип факта",
                             reply_markup=get_offer_facts_kb())
        await state.set_state(OfferFact.choosing_type_offer)
    else:
        facts = await get_offer_facts()
        await message.answer("Нажмите на предложенный факт, который вам понравился:",
                             reply_markup=get_offers_list(facts))
        await state.set_state(OfferFact.get_offer)


@router.message(OfferFact.get_offer, F.text)
async def get_offers(message: Message, state: FSMContext):
    text, fact_id, fact_type, subtype = message.text.split("_")
    await create_fact(fact_type=fact_type,
                      fact_subtype=subtype,
                      fact_text=text)
    await delete_offer_fact(int(fact_id))
    await message.answer("Добавлено в факты!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(OfferFact.choosing_type_offer, F.text.in_(fact_types))
async def choose_offer_type(message: Message, state: FSMContext):
    if message.text.lower() == "исторический факт":
        await state.update_data(choose_offer_type="historical")
        await message.reply("Выберите подтим факта",
                            reply_markup=get_historical_inline_kb())
        await state.set_state(OfferFact.choosing_subtype_offer)
    elif message.text.lower() == "научный факт":
        await state.update_data(choose_offer_type="science")
        await message.reply("Выберите подтим факта",
                            reply_markup=get_science_inline_kb())
        await state.set_state(OfferFact.choosing_subtype_offer)


@router.message(OfferFact.choosing_type_offer, F.text)
async def choose_type_fact_incorrect(message: Message):
    await message.answer(
        "Что-то пошло не так\n" "Воспользуйтесь кнопками!",
        reply_markup=get_offer_facts_kb()
    )


@router.callback_query(OfferFact.choosing_subtype_offer, F.data.in_(science_subfacts))
async def offer_science_fact(callback: CallbackQuery, state: FSMContext):
    await state.update_data(choose_type_subfact=callback.data)
    if callback.data == "math":
        await state.update_data(choose_offer_subtype="math")
        await callback.message.answer("Введите свой факт:",
                                      reply_markup=ReplyKeyboardRemove())
    elif callback.data == "bio":
        await state.update_data(choose_offer_subtype="bio")
        await callback.message.answer("Введите свой факт:",
                                      reply_markup=ReplyKeyboardRemove())
    elif callback.data == "space":
        await state.update_data(choose_offer_subtype="space")
        await callback.message.answer("Введите свой факт:",
                                      reply_markup=ReplyKeyboardRemove())

    await callback.answer()
    await state.set_state(OfferFact.create_offer)


@router.callback_query(OfferFact.choosing_subtype_offer,
                       F.data.in_(historical_subfacts))
async def offer_historical_fact(callback: CallbackQuery, state: FSMContext):
    await state.update_data(choose_type_subfact=callback.data)
    if callback.data == "old":
        await state.update_data(choose_offer_subtype="old")
        await callback.message.answer("Введите свой факт:",
                                      reply_markup=ReplyKeyboardRemove())
    elif callback.data == "mid":
        await state.update_data(choose_offer_subtype="mid")
        await callback.message.answer("Введите свой факт:",
                                      reply_markup=ReplyKeyboardRemove())
    elif callback.data == "20th":
        await state.update_data(choose_offer_subtype="20th")
        await callback.message.answer("Введите свой факт:",
                                      reply_markup=ReplyKeyboardRemove())

    await callback.answer()
    await state.set_state(OfferFact.create_offer)


@router.message(OfferFact.choosing_subtype_offer, F.text)
async def choose_type_subfact_incorrect(message: Message):
    await message.answer(
        "Что-то пошло не так\n" "Воспользуйтесь инлайн-кнопками!",
        reply_markup=get_offer_facts_kb()
    )


@router.message(OfferFact.create_offer, F.text)
async def create_offer(message: Message, state: FSMContext):
    await state.update_data(offer_text=message.text)
    offer_data = await state.get_data()
    print(offer_data)
    await create_offer_fact(fact_type=offer_data['choose_offer_type'],
                            fact_subtype=offer_data['choose_offer_subtype'],
                            fact_text=offer_data['offer_text'])

    await message.answer(text=f"Спасибо за предложение!\n"
                              f"Ваше предложение обработает модератор и, может быть в "
                              f"скором времени ваш факт появиться в нашем боте.")
    await state.clear()
