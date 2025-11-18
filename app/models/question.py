import datetime
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.orm import relationship, validates
from app.database import Base

class Question(Base):
    """
        Модель данных сущности Вопрос\n
        Содержит:
        id - идентификатор\n
        text - текст\n
        created_at - время создания\n
    """
    __tablename__="questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at =  Column(DateTime, default=datetime.datetime.now)

    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

    @validates('text')
    def validate_text(self, key, text):
        """Валидация поля text - не может быть пустым"""
        if not text or not text.strip():
            raise ValueError("Текст вопроса не может быть пустым")
        cleaned_text= text.strip()
        if len(cleaned_text)>10000:
            raise ValueError("Текст вопроса слишком длинный")
        if len(cleaned_text) < 2:
            raise ValueError("Текст вопроса слишком короткий")
        return cleaned_text