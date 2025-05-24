from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.models import Student, Score
from typing import Optional, List
class StudentCRUD:
    @staticmethod
    async def create_student(session: AsyncSession, telegram_id: int, first_name: str, last_name: str) -> Student:
        """Создание нового студента"""
        student = Student(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name
        )
        session.add(student)
        await session.commit()
        await session.refresh(student)
        return student

    @staticmethod
    async def get_student_by_telegram_id(session: AsyncSession, telegram_id: int) -> Optional[Student]:
        """Получение студента по Telegram ID"""
        result = await session.execute(
            select(Student).where(Student.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    @staticmethod
    async def student_exists(session: AsyncSession, telegram_id: int) -> bool:
        """Проверка существования студента"""
        student = await StudentCRUD.get_student_by_telegram_id(session, telegram_id)
        return student is not None
class ScoreCRUD:
    @staticmethod
    async def add_score(session: AsyncSession, student_id: int, subject: str, score: int) -> Score:
        """Добавление балла"""
        existing_score = await ScoreCRUD.get_score_by_subject(session, student_id, subject)
        if existing_score:
            existing_score.score = score
            await session.commit()
            await session.refresh(existing_score)
            return existing_score
        else:
            new_score = Score(
                student_id=student_id,
                subject=subject,
                score=score
            )
            session.add(new_score)
            await session.commit()
            await session.refresh(new_score)
            return new_score
    @staticmethod
    async def get_score_by_subject(session: AsyncSession, student_id: int, subject: str) -> Optional[Score]:
        """Получение балла по предмету"""
        result = await session.execute(
            select(Score).where(Score.student_id == student_id, Score.subject == subject)
        )
        return result.scalar_one_or_none()
    @staticmethod
    async def get_student_scores(session: AsyncSession, student_id: int) -> List[Score]:
        """Получение всех баллов студента"""
        result = await session.execute(
            select(Score).where(Score.student_id == student_id).order_by(Score.subject)
        )
        return result.scalars().all()