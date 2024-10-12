from datetime import datetime, timezone

from sqlalchemy import ForeignKey, TIMESTAMP, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def get_utc_time():
    '''Substitution for deprecated function `datetime.utcnow`'''
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        # server_default=func.now(),
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=get_utc_time,
    )


class KittenModel(Base):
    __tablename__ = 'kittens'

    color: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]
    description: Mapped[str | None]
    breed_id: Mapped[int] = mapped_column(ForeignKey('breeds.id'))
    breed: Mapped['BreedModel'] = relationship(back_populates='kittens')

    def __str__(self):
        return f'<{self.__class__.__name__}({self.id}), color:{self.color \
               }, age:{self.age}, breed_id:{self.breed_id}>'


class BreedModel(Base):
    __tablename__ = 'breeds'

    name: Mapped[str] = mapped_column(String(25))
    kittens: Mapped[list['KittenModel']] = relationship(back_populates='breed')

    def __str__(self):
        return f'<{self.__class__.__name__}({self.id}) {self.name}>'
