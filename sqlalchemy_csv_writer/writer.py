"""Provide SQLAlchemy Csv Writer."""
import csv
import typing
from typing import Union

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class SQLAlchemyCsvWriter:
    """Write SQL Alchemy results to a csv file."""

    def __init__(
        self,
        csvfile: typing.IO,
        write_header: bool = True,
        prefix_model_names: bool = False,
        field_formats: Union[dict[str, str], None] = None,
        *args,
        **kwargs,
    ):
        """Initialization.

        Args:
        csvfile: File-like object to write the resulting csv data to
        write_header: Whether to write the header
        prefix_model_names:  Whether to prefix the model names in the header
        field_formats: Dictionary containing the column name as keys and
                       column format as a values (using % style format syntax)
        *args: extra arguments to pass to csv.writer instance
        **kwargs: extra keyword arguments to pass to csv.writer instance
        """
        self.writer = csv.writer(csvfile, *args, **kwargs)
        self.write_header = write_header
        self.prefix_model_names = prefix_model_names
        self.field_formats = field_formats if field_formats else {}
        self.header_row_written = False

    async def write_rows_stream(self, results):
        """Write query results retrieved with SQLAlchemy's .stream or .stream_scalars.

        Args:
            results: query results retrieved with SQLAlchemy's .stream or .stream_scalars
        """
        async for result in results:
            self._process_result(result)

    def write_rows(self, results):
        """Write query results retrieved with SQLAlchemy's .execute or .scalars.

        Args:
            results: query results retrieved with SQLAlchemy's .execute or .scalars
        """
        for result in results:
            self._process_result(result)

    def _process_result(self, result):
        result = self._extract_columns(result)

        # write header
        if self.write_header and not self.header_row_written:
            self.writer.writerow([r[0] for r in result])
            self.header_row_written = True

        # write data
        values = []
        for key, value in result:
            if str(key) in self.field_formats:
                value = self.field_formats[str(key)] % value
            values.append(value)
        self.writer.writerow(values)

    def _extract_columns(self, result):
        columns = []
        if hasattr(result, "_mapping"):  # is not a scalar
            for element_key, element_value in result._mapping.items():
                if isinstance(element_value, DeclarativeBase):  # is an orm model
                    columns.extend(self._extract_model(element_value))
                else:  # is a column
                    columns.append((element_key, element_value))
        elif isinstance(result, DeclarativeBase):  # is a scalar orm model
            columns.extend(self._extract_model(result))

        return columns

    def _extract_model(self, obj):
        insp = inspect(obj)
        if self.prefix_model_names:
            return [(getattr(insp.class_, attr.key), attr.value) for attr in insp.attrs]
        else:
            return [(attr.key, attr.value) for attr in insp.attrs]
