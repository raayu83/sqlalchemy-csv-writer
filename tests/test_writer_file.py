from pathlib import Path

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


def test_write_with_string_path(db):
    with db.Session() as session:
        test_file = "test/test.csv"
        Path(test_file).unlink(missing_ok=True)

        results = session.scalars(select(User)).all()

        with SQLAlchemyCsvWriter(
            test_file,
            dialect="unix",
        ) as writer:
            writer.write_rows(results)

        expected_result = """"id","name","value"
"1","mary","12.31"
"2","joe","12.31"
"3","susan","12.31"
"""

        with open(test_file) as f:
            assert "".join(f.readlines()) == expected_result


def test_write_with_pathlib_path(db):
    with db.Session() as session:
        test_file = Path("test/test.csv")
        test_file.unlink(missing_ok=True)

        results = session.scalars(select(User)).all()

        with SQLAlchemyCsvWriter(
            test_file,
            dialect="unix",
        ) as writer:
            writer.write_rows(results)

        expected_result = """"id","name","value"
"1","mary","12.31"
"2","joe","12.31"
"3","susan","12.31"
"""

        with open(test_file) as f:
            assert "".join(f.readlines()) == expected_result
