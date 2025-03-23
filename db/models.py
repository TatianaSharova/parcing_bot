from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Source(Base):
    '''
    Модель для хранения информации о сайтах по продаже зюбликов.
    '''
    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    url: Mapped[str] = mapped_column(String(50), unique=True)
    xpath: Mapped[str] = mapped_column(String(50), nullable=False)
