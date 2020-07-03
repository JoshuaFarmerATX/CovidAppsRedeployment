import pandas as pd
import time
import datetime
import requests
import csv
from contextlib import closing
from flask import Flask, make_response, g

from sqlalchemy import Column, Float
from sqlalchemy.types import Date, BigInteger, Text
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from connection import conn_string_proxy, conn_string_deploy

Base = declarative_base()

app = Flask(__name__)

class USADailyCases(Base):
    __tablename__ = "usa_covid19"
    index = Column(BigInteger, primary_key=True)
    country_region = Column(Text)
    province_state = Column(Text)
    county_city = Column(Text)
    lat = Column(Float)
    long = Column(Float)
    date = Column(Date)
    confirmed = Column(BigInteger)
    deaths = Column(BigInteger)

@app.before_request
def before_request():
    g.request_start_time = time.time()

@app.route("/")
def load():

    connection_string = conn_string_proxy

    engine = create_engine(connection_string)

    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    # get most recent upload date to minimized sql transactions
    most_recent_date = session.query(func.max(USADailyCases.date)).all()[0][0]

    ### USA Covid19 Data
    
    usa_confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
    usa_deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
    
    with closing(requests.get(usa_confirmed_url, stream=True)) as confirmed_r, closing(
        requests.get(usa_deaths_url, stream=True)
    ) as deaths_r:

        confirmed_csv = csv.reader(
            confirmed_r.iter_lines(decode_unicode=True), delimiter=","
        )
        deaths_csv = csv.reader(deaths_r.iter_lines(decode_unicode=True), delimiter=",")
        
        csv_headers = list(next(confirmed_csv))
        next(deaths_csv)

        reporting_dates = [
            datetime.datetime.strptime(report_date, "%m/%d/%y").date()
            for report_date in csv_headers[11:]
        ]
        most_recent_date_index = reporting_dates.index(
            most_recent_date
        )  # add try except when checking for index/most recent

        for entry in zip(confirmed_csv, deaths_csv):
            confirmed_entry = entry[0]
            deaths_entry = entry[1]

            county_city = confirmed_entry[5]
            province_state = confirmed_entry[6]
            country_region = confirmed_entry[7]
            lat = confirmed_entry[8]
            long = confirmed_entry[9]

            if len(county_city) == 0:
                county_city = province_state

            for i, report_date in enumerate(
                reporting_dates[most_recent_date_index:],
                start=11 + most_recent_date_index
            ):
                record = USADailyCases(
                    **{
                        "country_region": country_region,
                        "province_state": province_state,
                        "county_city": county_city,
                        "lat": lat,
                        "long": long,
                        "date": report_date,
                        "confirmed": confirmed_entry[i],
                        "deaths": deaths_entry[i],                        
                    }
                )
                session.add(record)

    session.commit()
    session.close()
    engine.dispose()

    return make_response(
        f"Successful.\n Load Completion Time: {time.time()-g.request_start_time} s", 200
    )


if __name__ == "__main__":
    app.run(debug=True)
