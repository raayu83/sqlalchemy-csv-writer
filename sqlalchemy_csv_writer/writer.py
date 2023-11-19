"""Provide SQLAlchemy Csv Writer."""
import csv
import typing
from pathlib import Path
from typing import Union

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class SQLAlchemyCsvWriter:
    """Write SQL Alchemy results to a csv file."""

    def __init__(
        self,
        csvfile: Union[Path, str, typing.IO],
        header: Union[list[str], bool] = True,
        prefix_model_names: bool = False,
        field_formats: Union[dict[str, str], None] = None,
        dialect="excel",
        **fmtparams,
    ):
        """Create a SQLAlchemyCsvWriter instance.

        The instance's methods can be used to write rows to the specified csv file.

        Args:
            csvfile: Path or File-like object to write the resulting csv data to
            header: True to automatically generate header, False to disable header or list of strings for custom header
            prefix_model_names:  Whether to prefix the model names in the header
            field_formats: Dictionary containing the column name as keys and column format as a values (using % style format syntax)
            dialect: csv dialect to use
            **fmtparams: extra formatting parameters to pass to csv.writer instance
        """
        if isinstance(csvfile, str):
            csvfile = Path(csvfile)
        if isinstance(csvfile, Path):
            csvfile.parent.mkdir(exist_ok=True, parents=True)
            csvfile = open(csvfile, "w", encoding="utf-8")  # noqa: SIM115

        self.csvfile = csvfile
        self.writer = csv.writer(csvfile, dialect=dialect, **fmtparams)
        self.header = header
        self.prefix_model_names = prefix_model_names
        self.field_formats = field_formats if field_formats else {}
        self.header_row_written = False

    def __del__(self):
        """Close open resources."""
        if hasattr(self.csvfile, "close"):
            self.csvfile.close()

    def __enter__(self):
        """SQLAlchemyCsvWriter may be used as a context manager."""
        return self

    def __exit__(self, type, value, traceback):
        """Exit context manager."""
        self.__del__()

    async def write_rows_stream(self, results: list):
        """Write query results to csv.

        Write query results retrieved with SQLAlchemy's .stream or .stream_scalars.

        Args:
            results: query results retrieved with SQLAlchemy's .stream or .stream_scalars
        """
        async for result in results:
            self._process_result(result)

    def write_rows(self, results: list):
        """Write query results to csv.

        Write query results retrieved with SQLAlchemy's .execute or .scalars. to csv

        Args:
            results: query results retrieved with SQLAlchemy's .execute or .scalars
        """
        for result in results:
            self._process_result(result)

    def _process_result(self, result):
        result = self._extract_columns(result)

        # write header
        if self.header and not self.header_row_written:
            if self.header is True:
                self.writer.writerow([r[0] for r in result])
            else:
                if len(self.header) == len(result):
                    self.writer.writerow(self.header)
                else:
                    raise ValueError("Length of header and content does not match.")
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
