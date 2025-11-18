from sqlalchemy.orm import relationship, validates
from app.database import Base
from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

class Answer(Base):
    """
        Модель данных сущности Ответ\n
        Содержит:\n
        id - идентификатор\n
        question_id - ссылка на Question\n
        user_id - идентификатор пользователя, например uuid\n
        text - текст ответа\n
        created_at: время создания\n
    """
    __tablename__="answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), nullable=False)
    text = Column(Text, nullable=False)
    created_at=Column(DateTime, default=datetime.datetime.now)

    question=relationship("Question", back_populates="answers")

    @validates('text')
    def validate_text(self, key, text):
        """Валидация поля text - не может быть пустым"""
        if not text or not text.strip():
            raise ValueError("Текст ответа не может быть пустым")
        cleaned_text= text.strip()
        if len(cleaned_text)>10000:
            raise ValueError("Текст ответа слишком длинный")
        if len(cleaned_text) < 1:
            raise ValueError("Текст ответа слишком короткий")
        return cleaned_text
    
    @validates('user_id')
    def validate_user_id(self, key, user_id):
        """Валидация UUID пользователя"""
        if not user_id:
            raise ValueError("User ID не может быть пустым")
        try:
            uuid.UUID(user_id)
        except:
            raise ValueError("User ID должен быть валидным UUID")

        return user_id
    
    @validates('question_id')
    def validate_question_id(self, key, question_id):
        """Валидация ID вопроса"""
        if not question_id or question_id <= 0:
            raise ValueError("Question ID должен быть положительным числом")
        return question_id