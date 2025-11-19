from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate


class AnswerCRUD():
    def __init__(self, session: AsyncSession):
        self.session=session
    
    async def create_answer(self, answer: AnswerCreate, question_id :int)-> Answer:
        question=await self.session.get(Question, question_id)
        if not question:
            raise ValueError(f"Question with id {question_id} not found")
        answer_data=answer.model_dump()
        answer_data['question_id']=question_id
        db_answer=Answer(**answer_data)
        self.session.add(db_answer)
        await self.session.commit()
        await self.session.refresh(db_answer)
        return db_answer
    
    async def get_answer(self, answer_id: int)-> Answer| None:
        answer=await self.session.execute(select(Answer).where(Answer.id==answer_id))
        return answer.scalar_one_or_none()
    
    async def delete_answer(self, answer_id: int) -> bool:
        answer=await self.session.get(Answer, answer_id)
        if answer:
            await self.session.delete(answer)
            await self.session.commit()
            return True
        return False
