from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    password_hash: str
    role: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str | None = None
    password_hash: str | None = None
    role: str | None = None

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
