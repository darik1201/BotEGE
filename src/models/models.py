from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
Base = declarative_base()
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    scores = relationship("Score", back_populates="student", cascade="all, delete-orphan")
class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject = Column(String(100), nullable=False)
    score = Column(Integer, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="scores")