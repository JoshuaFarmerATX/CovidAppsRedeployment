import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
import sys
import os

sys.path.append(os.path.join(".."))

connection_string = sqlalchemy.engine.url.URL(
    drivername="mysql+pymysql",
    username="root",
    password="ehaarmanny",
    database="Covid",
    query={
        "unix_socket": "/cloudsql/{}".format("project-2-280623:us-central1:covid-db")
    },
)

engine = create_engine(connection_string, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
