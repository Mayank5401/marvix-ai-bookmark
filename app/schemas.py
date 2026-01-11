from pydantic import BaseModel ,EmailStr , Field ,ConfigDict


class ArticleCreate(BaseModel):
    title: str
    url: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class UserRead(BaseModel):
    id: int
    email: EmailStr

class TagRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

class ArticleRead(ArticleCreate):
    id: int
    title: str
    url: str
    tags: list[TagRead] = []
    model_config = ConfigDict(from_attributes=True)

class TagUpdate(BaseModel):
    tags: list[str]