from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    """Схема для создания нового пользователя"""
    name: str = Field(min_length=1, description="Имя пользователя")
    email: EmailStr = Field(description="Email адрес пользователя")


class UserResponse(BaseModel):
    """Схема для ответа с данными пользователя"""
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(UserResponse):
    """Схема для ответа с данными пользователя"""
    status: int
    description: str

