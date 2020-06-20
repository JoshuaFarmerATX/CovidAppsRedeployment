from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from .database import Base
import datetime


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


class Cases(Base, DictMixIn):
    __tablename__ = "daily_cases"

    index = Column(Integer, primary_key=True)
    iso3 = Column(String)
    country_region = Column(String)
    province_state = Column(String)
    lat = Column(Integer)
    long = Column(Integer)
    date = Column(Date)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)


class WorldTotalRecords(Base, DictMixIn):
    __tablename__ = "world_timeseries"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    total_confirmed = Column(Integer)
    total_deaths = Column(Integer)
    total_recovered = Column(Integer)


class Plot(Base, DictMixIn):
    __tablename__ = "plotting"

    index = Column(Integer, primary_key=True)
    country_region = Column(String)
    date = Column(Date)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    case_fatailty = Column(Float)
    iso3 = Column(String)
    older_pop = Column(Float)
