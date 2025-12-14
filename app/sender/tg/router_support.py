from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..locales import translation, try_get_translation as _


class SupportStates(StatesGroup):
    ASK_PROBLEM = State()       # Пользователь описывает проблему
    OFFER_SOLUTIONS = State()   # Предложение возможных вариантов действий
    SEND_TO_DEV = State()       # Решение отправить ошибку разработчикам
    CONNECT_SUPPORT = State()   # Связь со специалистом


router_support = Router(name="support")


@router_support.message(Command(commands=["support"]))
async def start_support_flow(message: Message, state: FSMContext):
    await message.answer(_("greeting"))
    await message.answer(_("describe_issue"))
    await state.set_state(SupportStates.ASK_PROBLEM)


@router_support.message(SupportStates.ASK_PROBLEM)
async def ask_problem(message: Message, state: FSMContext):
    problem_description = message.text.strip()
    await state.update_data(problem=problem_description)
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text=_("contact_support"),
                      callback_data="contact_support")
    kb_builder.button(text=_("send_to_developers"),
                      callback_data="send_to_dev")
    kb_builder.adjust(2)
    await message.answer(_("solution_choice"),
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(SupportStates.OFFER_SOLUTIONS)


@router_support.callback_query(SupportStates.OFFER_SOLUTIONS)
async def offer_solutions(query: CallbackQuery, state: FSMContext):
    if query.data == "contact_support":
        await query.message.edit_text(_("support_contacted"))
        await state.set_state(SupportStates.CONNECT_SUPPORT)
    elif query.data == "send_to_dev":
        data = await state.get_data()
        problem = data["problem"]
        await query.message.edit_text(_("issue_sent"))
        await state.set_state(SupportStates.SEND_TO_DEV)
    else:
        await query.answer(_("Неверный выбор. Попробуйте еще раз."), show_alert=True)
