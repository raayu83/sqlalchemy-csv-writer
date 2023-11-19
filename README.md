# SQLAlchemyCsvWriter

[![Stable Version](https://img.shields.io/pypi/v/sqlalchemy_csv_writer?label=stable)](https://pypi.org/project/sqlalchemy-csv-writer/#history)
![Python Versions](https://img.shields.io/pypi/pyversions/sqlalchemy_csv_writer)
![Tests](https://github.com/github/docs/actions/workflows/test.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/raayu83/sqlalchemy-csv-writer/graph/badge.svg?token=TXRKRRADUH)](https://codecov.io/gh/raayu83/sqlalchemy-csv-writer)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

SQLAlchemyCsvWriter is a thin wrapper around the python csw.writer function to make the process of exporting SQLAlchemy query results to csv simpler. 

It supports both synchronous as well as asynchronous query results, as well as streaming.

# Features
- Write SQLAlchemy query results to csv file with little boilerplate
- Optionally write header by auto generation or passing column names
- Supports same dialect and formatting parameters as [csv.writer](https://docs.python.org/3/library/csv.html#csv.writer)
- Supports synchronous, asynchronous and asynchronous streaming results
- Supports any models defined wit DeclarativeBase

# Installation
- with pip: `pip install sqlalchemy-csv-writer`
- with poetry: `poetry add sqlalchemy-csv-writer`

# Usage

```python
from sqlalchemy_csv_writer import SQLAlchemyCsvWriter

with SQLAlchemyCsvWriter(
    "test.csv",
    header=True,
    field_formats={"column_1": "%.2f"},
    prefix_model_names=True,
    dialect="unix",
) as writer:
    writer.write_rows(results)  # pass results of SQLAlchemy query
```

For full example see examples directory (uses the [alchemical](https://github.com/miguelgrinberg/alchemical) SQLAlchemy wrapper).

# Development Nots
- Linting and formatting using ruff
- Testing using pytest
- Dependency management and release using poetry
- Documentation using mkdocs with mkdocs-material and other plugins, released to GitHub pages
- CI/CD using GitHub Actions
- Pull requests are welcome