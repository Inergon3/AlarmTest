from app.config import user, password_bd, host, db_name
from sqlalchemy import Boolean, create_engine, ForeignKey, MetaData
from sqlalchemy.orm import as_declarative, mapped_column, Mapped, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_session

metadata = MetaData()
engine = create_async_engine(f"postgresql+asyncpg://{user}:{password_bd}@{host}/{db_name}", echo=True)
SessionLocal = async_session(engine)
# engine = create_engine(f"postgresql+asyncpg://{user}:{password_bd}@{host}/{db_name}", echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class AbstractModel:
    #id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    pass


class AlarmsModel(AbstractModel):
    __tablename__ = "alarm"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    alarm: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


class UsersModel(AbstractModel):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column()
    second_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    login: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
