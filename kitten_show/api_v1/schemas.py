from pydantic import BaseModel


class Breed(BaseModel):
    id: int
    name: str


class BaseKitten(BaseModel):
    color: str
    age: int
    description: str | None


class Kitten(BaseKitten):
    id: int
    breed: Breed


class CreateKitten(BaseKitten):
    breed_id: int


class UpdateKitten(BaseModel):
    color: str | None = None
    age: int | None = None
    description: str | None = None
    breed_id: int | None = None
