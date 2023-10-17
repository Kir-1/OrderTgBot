import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, Result

from ..texts import payment_text, log_payment_text
from src.core.models import User, Admin
from src.core import database
from ..keyboards import payment_menu
from ..states import Payment
from ..utils import CrystalpayKassa, broadcast

user_payment_router = Router()


@user_payment_router.message(Payment.input_amount)
async def payment_amount(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("Недопустимая сумма пополнения, Введите целое число")
        await state.clear()
        return

    cristal_pay = CrystalpayKassa()
    current_payment = cristal_pay.create_payment(int(message.text))

    await message.answer(
        text=await payment_text(amount=int(message.text), pay_id=current_payment["id"]),
        reply_markup=await payment_menu(current_payment["id"], current_payment["url"]),
    )

    with open("seolog.txt", "a", encoding="utf-8") as file:
        file.write(
            await log_payment_text(
                state="waiting",
                now=datetime.datetime.now(),
                external_id=message.from_user.id,
                user_name=message.from_user.username,
                pay_id=current_payment["id"],
                amount=int(message.text),
            )
        )


@user_payment_router.callback_query(F.data.startswith("Проверить оплату"))
async def payment_check(callback_query: CallbackQuery, state: FSMContext) -> None:
    cristal_pay = CrystalpayKassa()
    async with database.session_factory() as session:
        user = await session.get(User, {"id": callback_query.from_user.id})

        pay_id = callback_query.data.split(" ")[2]
        check_payment = cristal_pay.check_payment(pay_id)

        if check_payment["state"] != "payed":
            await callback_query.answer("Оплата не прошла")
            return

        await callback_query.answer("Оплата прошла успешно", show_alert=True)
        user.balance += check_payment["amount"]
        await session.commit()

    await callback_query.message.delete()

    async with database.session_factory() as session:
        stmt = select(Admin).where(Admin.is_available == True)
        result = await session.execute(stmt)
        admins = result.scalars().all()

    await broadcast(
        bot=callback_query.bot,
        model=Admin,
        ids=admins,
        text=await log_payment_text(
            state="broadcast",
            now=datetime.datetime.now(),
            external_id=callback_query.from_user.id,
            user_name=callback_query.from_user.username,
            pay_id=pay_id,
            amount=int(check_payment["amount"]),
            balance=user.balance,
            method=check_payment["method"],
            currency=check_payment["currency"],
        ),
    )

    with open("seolog.txt", "a", encoding="utf-8") as file:
        file.write(
            await log_payment_text(
                state="success",
                now=datetime.datetime.now(),
                external_id=callback_query.from_user.id,
                user_name=callback_query.from_user.username,
                pay_id=pay_id,
                amount=int(check_payment["amount"]),
                balance=user.balance,
                method=check_payment["method"],
                currency=check_payment["currency"],
            )
        )
