from sqlmodel import Field, SQLModel, create_engine

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    roleId: int = Field(default=1)
    username: str = Field(unique= True)
    password: str


