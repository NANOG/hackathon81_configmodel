"""Database models."""

import os
import tempfile

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

tempdir = tempfile.gettempdir()
sqlite_file = os.path.join(tempdir, "configmodel.db")
engine = create_engine("sqlite:///{}".format(sqlite_file), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
