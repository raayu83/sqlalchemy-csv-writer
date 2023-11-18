import asyncio
from io import StringIO

import pytest
from alchemical.aio import Alchemical
from sqlalchemy import select

from sqlalchemy_csv_writer import SQLAlchemyCsvWriter
from tests.model import User


@pytest.fixture(scope="module")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def db():
    db = Alchemical("sqlite:///:memory:")
    await db.drop_all()
    await db.create_all()

    async with db.begin() as session:
        for name in ["mary", "joe", "susan"]:
            session.add(User(name=name, value=12.31))

    return db


async def test_write_rows_with_stream_scalars_with_prefixed_header_and_formatting(db):
    async with db.Session() as session:
        stringio = StringIO()
        results = await session.stream_scalars(select(User))

        field_formats = {"User.value": "%.1f"}
        writer = SQLAlchemyCsvWriter(
            stringio,
            field_formats=field_formats,
            prefix_model_names=True,
            dialect="unix",
        )
        await writer.write_rows_stream(results)

        expected_result = """"User.id","User.name","User.value"
"1","mary","12.3"
"2","joe","12.3"
"3","susan","12.3"
"""

        assert stringio.getvalue() == expected_result


async def test_write_rows_with_stream_with_header(db):
    async with db.Session() as session:
        stringio = StringIO()
        results = await session.stream(select(User))

        writer = SQLAlchemyCsvWriter(
            stringio,
            dialect="unix",
        )
        await writer.write_rows_stream(results)

        expected_result = """"id","name","value"
"1","mary","12.31"
"2","joe","12.31"
"3","susan","12.31"
"""

        assert stringio.getvalue() == expected_result


async def test_write_rows_with_stream_without_header(db):
    async with db.Session() as session:
        stringio = StringIO()
        results = await session.stream(select(User))

        writer = SQLAlchemyCsvWriter(
            stringio,
            write_header=False,
            dialect="unix",
        )
        await writer.write_rows_stream(results)

        expected_result = """"1","mary","12.31"
"2","joe","12.31"
"3","susan","12.31"
"""

        assert stringio.getvalue() == expected_result


async def test_write_rows_with_scalars_with_prefixed_header_and_formatting(db):
    async with db.Session() as session:
        stringio = StringIO()
        results = await session.scalars(select(User))

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


async def test_write_rows_with_execute_with_header(db):
    async with db.Session() as session:
        stringio = StringIO()
        results = await session.execute(select(User))

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


async def test_write_rows_with_execute_without_header(db):
    async with db.Session() as session:
        stringio = StringIO()
        results = await session.execute(select(User))

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
