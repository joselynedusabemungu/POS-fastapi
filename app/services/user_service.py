from repositories import user_repository
from schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_user(db:Session, user_id:int):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def list_user(db: Session):
    return user_repository.get_all(db)

def create_user(db:Session, user:UserCreate):
    return user_repository.create(db, user.model_dump())

def update_user(db: Session, user_id: int, user: UserUpdate):
    retrieved_user = get_user(db, user_id)
    updated_user = user_repository.update(db, retrieved_user, user.model_dump(exclude_unset=True))
    return updated_user

def delete_user(db: Session, user_id: int):
    deleted_user = get_user(db, user_id)
    try:
        return user_repository.delete(db, deleted_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot delete User {user_id}: it is still referenced by other records",
        )