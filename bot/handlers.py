from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from bot.db import (reset_quiz_state, get_quiz_index, update_quiz_index,
                    update_correct_answers, get_correct_answers,
                    update_quiz_result, get_quiz_result)

def generate_options_keyboard(answer_options, question_id):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"{question_id}:{option}")
        )

    builder.adjust(1)
    return builder.as_markup()

def register_handlers(dp, quiz_data):
    @dp.callback_query()
    async def handle_answer(callback: types.CallbackQuery):
        user_answer = callback.data.split(":")
        question_id = int(user_answer[0])
        selected_option = user_answer[1]

        correct_option = quiz_data[question_id]['options'][quiz_data[question_id]['correct_option']]
        is_correct = selected_option == correct_option

        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )

        if is_correct:
            await callback.message.answer("Верно!")
            await update_correct_answers(callback.from_user.id, 1)
        else:
            await callback.message.answer(f"Неправильно. Правильный ответ: {correct_option}")

        await callback.message.answer(f"Ваш ответ: {selected_option}")

        current_question_index = await get_quiz_index(callback.from_user.id)
        current_question_index += 1
        await update_quiz_index(callback.from_user.id, current_question_index)

        if current_question_index < len(quiz_data):
            await get_question(callback.message, callback.from_user.id, quiz_data)
        else:
            correct_answers = await get_correct_answers(callback.from_user.id)
            await update_quiz_result(callback.from_user.id, correct_answers, len(quiz_data))
            await callback.message.answer(f"Это был последний вопрос. Квиз завершен! Ваш результат: {correct_answers} из {len(quiz_data)}")

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать игру"))
        builder.add(types.KeyboardButton(text="Статистика"))
        await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

    @dp.message(F.text == "Начать игру")
    @dp.message(Command("quiz"))
    async def cmd_quiz(message: types.Message):
        await message.answer(f"Давайте начнем квиз!")
        await new_quiz(message, quiz_data)

    @dp.message(F.text == "Статистика")
    @dp.message(Command("stats"))
    async def cmd_stats(message: types.Message):
        user_id = message.from_user.id
        result = await get_quiz_result(user_id)
        if result:
            correct_answers, total_questions = result
            await message.answer(f"Ваш последний результат: {correct_answers} из {total_questions}")
        else:
            await message.answer("Вы еще не прошли ни одного квиза.")

async def new_quiz(message, quiz_data):
    user_id = message.from_user.id
    await reset_quiz_state(user_id)
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id, quiz_data)

async def get_question(message, user_id, quiz_data):
    current_question_index = await get_quiz_index(user_id)
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, current_question_index)
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb, parse_mode="MarkdownV2")
