from io import StringIO

import pytest
from alchemical import Alchemical
from sqlalchemy import select

from sqlalchemy_csv_writer import SQLAlchemyCsvWriter
from tests.model import User


@pytest.fixture(scope="module")
def db():
    db = Alchemical("sqlite:///:memory:")
    db.drop_all()
    db.create_all()

    with db.begin() as session:
        for name in ["mary", "joe", "susan"]:
            session.add(User(name=name, value=12.31))
    return db


def test_write_rows_with_scalars_with_prefixed_header_and_formatting(db):
    with db.Session() as session:
        stringio = StringIO()
        results = session.scalars(select(User)).all()

        field_formats = {"User.value": "%.1f"}
        writer = SQLAlchemyCsvWriter(
            stringio,
            field_formats=field_formats,
            prefix_model_names=True,
            dialect="unix",
        )
        writer.write_rows(results)

        expected_result = """"User.id","User.name","User.value"
"1","mary","12.3"
"2","joe","12.3"
"3","susan","12.3"
"""

        assert stringio.getvalue() == expected_result


def test_write_rows_with_execute_with_header(db):
    with db.Session() as session:
        stringio = StringIO()
        results = session.execute(select(User)).all()

        writer = SQLAlchemyCsvWriter(
            stringio,
            dialect="unix",
        )
        writer.write_rows(results)

        expected_result = """"id","name","value"
"1","mary","12.31"
"2","joe","12.31"
"3","susan","12.31"
"""

        assert stringio.getvalue() == expected_result


def test_write_rows_with_execute_without_header(db):
    with db.Session() as session:
        stringio = StringIO()
        results = session.execute(select(User)).all()

        writer = SQLAlchemyCsvWriter(
            stringio,
            write_header=False,
            dialect="unix",
        )
        writer.write_rows(results)

        expected_result = """"1","mary","12.31"
"2","joe","12.31"
"3","susan","12.31"
"""

        assert stringio.getvalue() == expected_result


def test_write_rows_with_execute_with_duplicate_columns(db):
    with db.Session() as session:
        stringio = StringIO()
        results = session.execute(select(User, User)).all()

        writer = SQLAlchemyCsvWriter(
            stringio,
            write_header=True,
            dialect="unix",
        )
        writer.write_rows(results)

        expected_result = """"id","name","value","id","name","value"
"1","mary","12.31","1","mary","12.31"
"2","joe","12.31","2","joe","12.31"
"3","susan","12.31","3","susan","12.31"
"""

        assert stringio.getvalue() == expected_result
