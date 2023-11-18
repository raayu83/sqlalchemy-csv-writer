from alchemical import Model
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class User(Model):
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    value: Mapped[float] = mapped_column()