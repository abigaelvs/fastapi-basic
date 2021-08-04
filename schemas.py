from typing import List, Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str
    owner_id: int


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class Article(ArticleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    gender: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_authenticated: bool
    articles: List[Article] = []

    class Config:
        orm_mode = True