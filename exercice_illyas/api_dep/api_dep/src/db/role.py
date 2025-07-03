from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

from sqlalchemy import Column, func
from sqlalchemy.sql.sqltypes import DateTime


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    createdAt : datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
