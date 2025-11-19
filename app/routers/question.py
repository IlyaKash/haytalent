from fastapi import Depends, APIRouter, HTTPException, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionWithAnswersResponse
from app.crud.question_crud import QuestionCRUD

from app.crud.answer_crud import AnswerCRUD
from app.routers.answer import get_answer_crud

router=APIRouter()

async def get_question_crud(db: AsyncSession = Depends(get_async_session)) -> QuestionCRUD:
    return QuestionCRUD(db)

@router.post(
    "/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    description="Создать новый вопрос"
)
async def create_qestion(
    question: QuestionCreate,
    crud: QuestionCRUD= Depends(get_question_crud)
):
    try:
        new_question=await crud.create(question)
        return new_question
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[QuestionResponse],
    description="Возвращает список вопросов"
)
async def read_questions(
    skip: int=Query(0, ge=0, description="Количество пропущенных записей"),
    limit : int=Query(100, ge=1, le=100, description="Максимальное количество записей"),
    crud: QuestionCRUD=Depends(get_question_crud)
):
    questions=await crud.get_all_qestions()
    return questions[skip:skip+limit]

@router.get(
    "/{id}",
    response_model=QuestionWithAnswersResponse,
    description="Возвращает вопрос и все ответы к нему"
)
async def read_question(
    id: int,
    crud: QuestionCRUD=Depends(get_question_crud)
):
    question=await crud.get_qestion_with_answers(id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return question

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    description="Удаляет вопрос и все ответы к нему"
)
async def delete_question(
    id: int,
    crud: QuestionCRUD=Depends(get_question_crud)
):
    success=await crud.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The question not found"
        )
    return {
        "success" : True, "message" : "Question deleted successfully"
    }

@router.post(
    "/{id}/answers/",
    response_model=AnswerResponse,
    description="Добавляет ответ конкретному вопросу"
)
async def create_answer_for_question(
    id: int,
    answer: AnswerCreate,
    answer_crud: AnswerCRUD = Depends(get_answer_crud),
    question_crud: QuestionCRUD=Depends(get_question_crud)
):
    question_exists= await question_crud.get_qestion_with_answers(id)
    if not question_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The question with ID {id} not found"
        )
    
    try:
        return await answer_crud.create_answer(answer, id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating answer {str(e)}"
        )