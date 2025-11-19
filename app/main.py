from fastapi import FastAPI
from app.routers.answer import router as answer_router
from app.routers.question import router as question_router

app=FastAPI(
    title="Haytalent API",
    version="1.0.0"
)

app.include_router(router=question_router, prefix="/questions", tags=["questions"])
app.include_router(router=answer_router, prefix="/answers", tags=["answers"])

@app.get("/")
async def root():
    return {
        "message": "Haytalent API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
