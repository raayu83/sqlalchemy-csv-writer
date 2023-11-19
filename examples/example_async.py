import asyncio
from io import StringIO

from alchemical.aio import Alchemical, Model
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy_csv_writer import SQLAlchemyCsvWriter


class User(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    value: Mapped[float] = mapped_column()


async def run():
    db = Alchemical("sqlite:///:memory:")
    await db.drop_all()
    await db.create_all()

    async with db.begin() as session:
        for name in ["mary", "joe", "susan"]:
            session.add(User(name=name, value=12.3))

    async with db.Session() as session:
        stringio = StringIO()
        results = await session.execute(select(User))

        field_formats = {"value": "%.2f"}
        writer = SQLAlchemyCsvWriter(
            stringio,
            header=True,
            field_formats=field_formats,
            dialect="unix",
        )
        writer.write_rows(results)

        print(stringio.getvalue())


asyncio.run(run())
