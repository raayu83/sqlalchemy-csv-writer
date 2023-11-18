SQLAlchemyCsvWriter
=====================

SQLAlchemyCsvWriter is a thin wrapper around the python csw.writer function to make the process of exporting 
SQLAlchemy query results to csv simpler. 

It supports both synchronous as well as asynchronous query results, as well as streaming.

.. code-block:: python

    from sqlalchemy_csv_writer import SQLAlcehmyCSVWriter

    writer = SQLAlchemyCsvWriter(
        stringio,
        write_header=True,
        field_formats=field_formats,
        prefix_model_names=True,
        dialect="unix",
    )
    writer.writerrows(results) # pass result of SQLAlchemy query