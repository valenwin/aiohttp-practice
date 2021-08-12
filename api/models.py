import contextvars

import sqlalchemy as sa
import ujson
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = sa.MetaData(naming_convention=convention)
Model = declarative_base(metadata=metadata)
Session = sessionmaker(class_=AsyncSession)

session_context = contextvars.ContextVar("session")


async def db_disconnect():
    pass


async def db_connect(database_uri, echo: bool = False):
    Session.configure(
        bind=create_async_engine(
            database_uri,
            echo=echo,
            json_serializer=ujson.dumps,
            json_deserializer=ujson.loads,
        )
    )


class Base(Model):
    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)


class Book(Base):
    __tablename__ = "books_book"

    name = sa.Column(sa.String(50), nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.text("NOW()"))
    author_id = sa.Column(
        sa.ForeignKey("books_author.id", deferrable=True, initially="DEFERRED"),
        nullable=True,
        index=True,
    )


class Author(Base):
    __tablename__ = "books_author"

    name = sa.Column(sa.String(50), nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.text("NOW()"))
