from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models.question import Question
from app.schemas.question import QuestionCreate

class QuestionCRUD():
    def __init__(self, session: AsyncSession):
        self.session=session
    
    async def create(self, question: QuestionCreate)->Question:
        db_question=Question(**question.model_dump())
        self.session.add(db_question)
        await self.session.commit()
        await self.session.refresh(db_question)
        
        #result= await self.session.execute(
        #    select(Question)
        #    .options(selectinload(Question.answers))
        #    .where(Question.id==db_question.id)
        #)
        #db_question=result.scalar_one()
        return db_question
    
    async def get_qestion_with_answers(self, question_id: int)-> Question:
        result = await self.session.execute(
                select(Question)
                .options(selectinload(Question.answers))
                .where(Question.id == question_id)
            )
        return result.scalar_one_or_none()
    
    async def get_all_qestions(self)-> list[Question]:
        result=await self.session.execute(
            select(Question)
        )
        return result.scalars().all()
    
    async def delete(self, question_id: int)->bool:
        question=await self.session.get(Question, question_id)
        if question:
            await self.session.delete(question)
            await self.session.commit()
            return True
        return False