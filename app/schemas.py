from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class RatingOut(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class MovieOut(BaseModel):
    id: int
    show_id: str
    type: Optional[str]
    title: str
    director: Optional[str]
    cast: Optional[str]
    country: Optional[str]
    date_added: Optional[date]
    release_year: Optional[int]
    rating: Optional[str]
    duration: Optional[str]
    description: Optional[str]
    categories: List[CategoryOut] = []
    rating_rel: Optional[RatingOut]

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str