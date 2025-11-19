from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.crud.answer_crud import AnswerCRUD
from app.schemas.answer import AnswerResponse


router=APIRouter()

async def get_answer_crud(db: AsyncSession=Depends(get_async_session))->AnswerCRUD:
    return AnswerCRUD(db)

@router.get(
    "/{id}",
    response_model=AnswerResponse,
    description="Возвращает конкретный ответ"
)
async def read_answer(
    id: int,
    crud: AnswerCRUD=Depends(get_answer_crud)
):
    answer=await crud.get_answer(id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    return answer

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    description="Удаляет ответ"
)
async def delete_answer(
    id: int,
    crud: AnswerCRUD=Depends(get_answer_crud)
):
    success=await crud.delete_answer(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The answer not found"
        )
    return {
        "success" : True, "message" : "The answer deleted successfully"
    }