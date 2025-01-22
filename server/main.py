from contextlib import asynccontextmanager

import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.task import TaskCreate
from core.models import Task
from core.models.db_helper import db_helper
from crud.task import get_task, create_task, update_task



def run_migrations() -> bool:
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        
        return True
    except Exception as e:
        print(e)
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield
    
    await db_helper.disponse()


main_app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://66.90.102.54",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_app.get("/tasks")
async def get_tasks(session: AsyncSession = Depends(db_helper.session_getter)):
    return await get_task(session)

@main_app.post("/tasks")
async def post_tasks(task: TaskCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    return await create_task(session, task)

@main_app.put("/tasks/{task_id}")
async def put_tasks(task_id: int, task: TaskCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    return await update_task(session, task_id, task)




if __name__ == "__main__":
    if not run_migrations():
        print("Таблица не создалась")
    uvicorn.run(main_app, host="0.0.0.0", port=8000)