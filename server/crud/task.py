from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import Select
from sqlalchemy.exc import IdentifierError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas.task import TaskCreate


async def get_task(
    session: AsyncSession
) -> Sequence[Task]:
    stmt = Select(Task).order_by(Task.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_task(
    session: AsyncSession,
    task: TaskCreate
):
    new_item = Task(**task.model_dump())
    
    try:
        session.add(new_item)
        await session.commit()
    except IndentationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return new_item

async def update_task(
    session: AsyncSession,
    task_id: int,
    task: TaskCreate
):
    stmt = Select(Task).where(Task.id == task_id)
    result: Task = (await session.execute(stmt)).scalar_one_or_none()
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    result.description = task.description
    
    await session.commit()
    await session.refresh()
    return result
    