from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List
from datetime import datetime
from .answer import AnswerResponse

class QuestionBase(BaseModel):
    text: str =Field(
        ...,
        min_length=1,
        max_length=10000,
        examples=["Почему небо синeе?", "Почему тучка плачет?"],
        description="Question text"
    )
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Валидация текста вопроса"""
        if not v or not v.strip():
            raise ValueError("Текст вопроса не может быть пустым")
        
        cleaned_text = v.strip()
        
        if len(cleaned_text) < 3:
            raise ValueError("Текст вопроса слишком короткий")
            
        if len(cleaned_text) > 10000:
            raise ValueError("Текст вопроса слишком длинный")
            
        return cleaned_text

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id : int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class QuestionWithAnswersResponse(QuestionResponse):
    """Вопрос со списком ответов"""
    answers: List[AnswerResponse] = Field(
        default_factory=[],
        description="List of answers"
    )