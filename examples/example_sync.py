from io import StringIO

from alchemical import Alchemical, Model
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy_csv_writer import SQLAlchemyCsvWriter


class User(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    value: Mapped[float] = mapped_column()


db = Alchemical("sqlite:///:memory:")
db.drop_all()
db.create_all()

with db.begin() as session:
    for name in ["mary", "joe", "susan"]:
        session.add(User(name=name, value=12.3))

with db.Session() as session:
    stringio = StringIO()
    results = session.execute(select(User)).all()

    field_formats = {"value": "%.2f"}
    writer = SQLAlchemyCsvWriter(
        stringio,
        write_header=True,
        field_formats=field_formats,
        prefix_model_names=True,
        dialect="unix",
    )
    writer.writerrows(results)

    print(stringio.getvalue())
