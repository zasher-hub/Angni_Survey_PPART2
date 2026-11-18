from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str

class Drink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class UserLogin(SQLModel):
    username: str
    password: str