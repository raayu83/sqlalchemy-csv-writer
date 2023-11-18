# SQLAlchemyCsvWriter

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Stable Version](https://img.shields.io/pypi/v/sqlalchemy_csv_writer?label=stable)][PyPI Releases]
[![Python Versions](https://img.shields.io/pypi/pyversions/sqlalchemy_csv_writer)][PyPI]
![Tests](https://github.com/github/docs/actions/workflows/test.yml/badge.svg?branch=main)

SQLAlchemyCsvWriter is a thin wrapper around the python csw.writer function to make the process of exporting 
SQLAlchemy query results to csv simpler. 

It supports both synchronous as well as asynchronous query results, as well as streaming.

```python
    from io import StringIO
    from sqlalchemy_csv_writer import SQLAlchemyCsvWriter

    stringio = StringIO()
    writer = SQLAlchemyCsvWriter(
        stringio,
        write_header=True,
        field_formats={"column_1": "%.2f"},
        prefix_model_names=True,
        dialect="unix",
    )
    writer.writerrows(results) # pass result of SQLAlchemy query
```