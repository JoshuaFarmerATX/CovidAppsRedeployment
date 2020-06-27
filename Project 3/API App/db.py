import datetime

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(getattr(self, column.name), datetime.datetime)
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


class GlobalDailyCases(Base, DictMixIn):
    __tablename__ = "daily_cases"
    index = Column(Integer, primary_key=True, nullable=False)
    country_region = Column(String)
    province_state = Column(String)
    lat = Column(Float)
    long = Column(Float)
    date = Column(Date)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    iso3 = Column(String)


class USADailyCases(Base, DictMixIn):
    __tablename__ = "usa_covid19"
    index = Column(Integer, primary_key=True)
    country_region = Column(String)
    province_state = Column(String)
    county_city = Column(String)
    lat = Column(Float)
    long = Column(Float)
    date = Column(Date)
    confirmed = Column(Integer)
    deaths = Column(Integer)


if __name__ == "__main__":
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine

    from connection import conn_string_proxy

    engine = create_engine(conn_string_proxy)
    global_daily_cases_db = Session(engine)
    print(
        [
            val.to_dict()
            for val in global_daily_cases_db.query(GlobalDailyCases).filter(
                GlobalDailyCases.iso3 == "BRA"
            )
        ]
    )
