from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import List
from datetime import datetime

class AnswerBase(BaseModel):
    user_id : str=Field(
        ...,
        min_length=1,
        max_length=36,
        examples=["3422b448-2460-4fd2-9183-8000de6f8343"],
        description="User UUID"
    )

    text: str =Field(
        ...,
        min_length=3,
        max_length=10000,
        examples=["Потому что.", "Потому что тучке грустно."],
        description="Question text"
    )

class AnswerCreate(AnswerBase):
    #question_id: int = Field(
    #    ... ,
    #    examples=[1, 2, 3],
    #    description="The identifier of the qestion to which the answer is linked"
    #)
    pass

class AnswerResponse(AnswerCreate):
    id : int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)