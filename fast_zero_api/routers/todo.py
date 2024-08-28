from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_api.database import get_session
from fast_zero_api.models import Todo, User
from fast_zero_api.schema import Message, TodoList, TodoPublic, TodoSchema, TodoUpdate
from fast_zero_api.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]

# usuario logado na API
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, session: T_Session, user: T_CurrentUser):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(
    session: T_Session,
    user: T_CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}  # o retorno é compatível com o schema TodoList


@router.delete('/delete/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: T_CurrentUser):
    todo = session.scalar(select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id))

    if not todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/update/{todo_id}', response_model=TodoPublic)
def update_todo(todo_id: int, session: T_Session, user: T_CurrentUser, todo: TodoUpdate):
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not db_todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
