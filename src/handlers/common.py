from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.states.states import RegistrationStates, ScoreStates
from src.crud.crud import StudentCRUD, ScoreCRUD
from src.keyboards.keyboards import get_main_menu, get_subjects_keyboard
router = Router()
@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession):
    """Обработчик команды /start"""
    telegram_id = message.from_user.id
    if await StudentCRUD.student_exists(session, telegram_id):
        student = await StudentCRUD.get_student_by_telegram_id(session, telegram_id)
        await message.answer(
            f"Добро пожаловать обратно, {student.first_name} {student.last_name}!\n\n"
            "Выберите действие из меню:",
            reply_markup=get_main_menu()
        )
    else:
        await message.answer(
            "Добро пожаловать в бот для сбора баллов ЕГЭ!\n\n"
            "Для начала работы необходимо зарегистрироваться.\n"
            "Используйте команду /register для регистрации."
        )
@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext, session: AsyncSession):
    """Обработчик команды /register"""
    telegram_id = message.from_user.id
    if await StudentCRUD.student_exists(session, telegram_id):
        await message.answer(
            "Вы уже зарегистрированы!\n"
            "Используйте меню для работы с баллами.",
            reply_markup=get_main_menu()
        )
        return
    await message.answer("Давайте зарегистрируем вас в системе!\n\nВведите ваше имя:")
    await state.set_state(RegistrationStates.waiting_for_first_name)
@router.message(StateFilter(RegistrationStates.waiting_for_first_name))
async def process_first_name(message: Message, state: FSMContext):
    """Обработка ввода имени"""
    first_name = message.text.strip()
    if not first_name or len(first_name) < 2:
        await message.answer("Пожалуйста, введите корректное имя (минимум 2 символа):")
        return
    await state.update_data(first_name=first_name)
    await message.answer("Отлично! Теперь введите вашу фамилию:")
    await state.set_state(RegistrationStates.waiting_for_last_name)
@router.message(StateFilter(RegistrationStates.waiting_for_last_name))
async def process_last_name(message: Message, state: FSMContext, session: AsyncSession):
    """Обработка ввода фамилии"""
    last_name = message.text.strip()
    if not last_name or len(last_name) < 2:
        await message.answer("Пожалуйста, введите корректную фамилию (минимум 2 символа):")
        return
    data = await state.get_data()
    first_name = data['first_name']
    try:
        student = await StudentCRUD.create_student(
            session,
            message.from_user.id,
            first_name,
            last_name
        )
        await message.answer(
            f"Регистрация прошла успешно!\n\n"
            f"Добро пожаловать, {first_name} {last_name}!\n"
            f"Теперь вы можете использовать все функции бота.",
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await message.answer(
            "Произошла ошибка при регистрации. Попробуйте еще раз.\n"
            "Используйте команду /register"
        )
    await state.clear()
@router.message(F.text == "Ввести баллы")
@router.message(Command("enter_scores"))
async def enter_scores(message: Message, state: FSMContext, session: AsyncSession):
    """Обработчик ввода баллов"""
    telegram_id = message.from_user.id
    if not await StudentCRUD.student_exists(session, telegram_id):
        await message.answer(
            "Вы не зарегистрированы! Используйте команду /register для регистрации."
        )
        return
    await message.answer(
        "Выберите предмет, по которому хотите ввести балл:",
        reply_markup=get_subjects_keyboard()
    )
@router.callback_query(F.data.startswith("subject_"))
async def process_subject_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора предмета"""
    subject = callback.data.replace("subject_", "")
    await state.update_data(subject=subject)
    await callback.message.edit_text(
        f"Вы выбрали предмет: {subject}\n\n"
        f"Введите ваш балл (от 0 до 100):"
    )
    await state.set_state(ScoreStates.waiting_for_score)
    await callback.answer()
@router.message(StateFilter(ScoreStates.waiting_for_score))
async def process_score_input(message: Message, state: FSMContext, session: AsyncSession):
    """Обработка ввода балла"""
    try:
        score = int(message.text.strip())
        if not (0 <= score <= 100):
            await message.answer("Балл должен быть от 0 до 100. Попробуйте еще раз:")
            return
        data = await state.get_data()
        subject = data['subject']
        student = await StudentCRUD.get_student_by_telegram_id(session, message.from_user.id)
        await ScoreCRUD.add_score(session, student.id, subject, score)
        await message.answer(
            f"Балл успешно сохранен!\n\n"
            f"Предмет: {subject}\n"
            f"Балл: {score}",
            reply_markup=get_main_menu()
        )
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число от 0 до 100:")
@router.message(F.text == "Мои баллы")
@router.message(Command("view_scores"))
async def view_scores(message: Message, session: AsyncSession):
    """Обработчик просмотра баллов"""
    telegram_id = message.from_user.id
    student = await StudentCRUD.get_student_by_telegram_id(session, telegram_id)
    if not student:
        await message.answer(
            "Вы не зарегистрированы! Используйте команду /register для регистрации."
        )
        return
    scores = await ScoreCRUD.get_student_scores(session, student.id)
    if not scores:
        await message.answer(
            "У вас пока нет сохраненных баллов.\n"
            "Используйте кнопку 'Ввести баллы' для добавления результатов.",
            reply_markup=get_main_menu()
        )
        return
    scores_text = f"Ваши баллы ЕГЭ:\n\n"
    total_score = 0
    for score in scores:
        scores_text += f"{score.subject}: {score.score} баллов\n"
        total_score += score.score
    scores_text += f"\n📈 Общая сумма баллов: {total_score}"
    await message.answer(scores_text, reply_markup=get_main_menu())
@router.message(F.text == "Помощь")
async def help_command(message: Message):
    """Обработчик помощи"""
    help_text = (
        "Помощь по использованию бота:\n\n"
        "Доступные команды:\n"
        "/start - Начало работы с ботом\n"
        "/register - Регистрация в системе\n"
        "/enter_scores - Ввод баллов ЕГЭ\n"
        "/view_scores - Просмотр ваших баллов\n\n"
        "Как использовать:\n"
        "1. Зарегистрируйтесь командой /register\n"
        "2. Вводите баллы по предметам\n"
        "3. Просматривайте результаты\n\n"
        "💡 Баллы можно обновлять - новый балл заменит старый по тому же предмету."
    )
    await message.answer(help_text, reply_markup=get_main_menu())
