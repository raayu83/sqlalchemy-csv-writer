from alchemical import Model
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    value: Mapped[float] = mapped_column()
