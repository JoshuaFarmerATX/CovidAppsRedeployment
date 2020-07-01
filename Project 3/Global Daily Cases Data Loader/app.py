import time
import datetime
import requests
import csv
from contextlib import closing
import country_converter as coco
from flask import Flask, make_response, g

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date, BigInteger, Text
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from connection import conn_string_proxy, conn_string_deploy

Base = declarative_base()


class GlobalDailyCases(Base):
    __tablename__ = "daily_cases"
    index = Column(BigInteger, primary_key=True, nullable=False)
    country_region = Column(Text)
    province_state = Column(Text)
    lat = Column(Float)
    long = Column(Float)
    date = Column(Date)
    confirmed = Column(BigInteger)
    deaths = Column(BigInteger)
    recovered = Column(Integer)
    iso3 = Column(Text)


app = Flask(__name__)


@app.before_request
def before_request():
    g.request_start_time = time.time()


@app.route("/")
def load():

    # Connect to the "Covid" database

    # Change connection_string to conn_string_proxy when connecting locally
    # via proxy and to conn_string_deploy when being uploaded for GCP.

    connection_string = conn_string_deploy

    engine = create_engine(connection_string)

    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    # get most recent upload date to minimized sql transactions
    most_recent_date = session.query(func.max(GlobalDailyCases.date)).all()[0][0]

    coco.logging.getLogger().setLevel(coco.logging.CRITICAL)

    ### World Data
    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

    with closing(requests.get(confirmed_url, stream=True)) as confirmed_r, closing(
        requests.get(deaths_url, stream=True)
    ) as deaths_r, closing(requests.get(recovered_url, stream=True)) as recovered_r:

        confirmed_csv = csv.reader(
            confirmed_r.iter_lines(decode_unicode=True), delimiter=","
        )
        deaths_csv = csv.reader(deaths_r.iter_lines(decode_unicode=True), delimiter=",")
        recovered_csv = csv.reader(
            recovered_r.iter_lines(decode_unicode=True), delimiter=","
        )

        csv_headers = list(next(confirmed_csv))
        next(deaths_csv)
        next(recovered_csv)

        reporting_dates = [
            datetime.datetime.strptime(report_date, "%m/%d/%y").date()
            for report_date in csv_headers[4:]
        ]
        most_recent_date_index = reporting_dates.index(
            most_recent_date
        )  # add try except when checking for index/most recent

        cc = coco.CountryConverter()

        for entry in zip(confirmed_csv, deaths_csv, recovered_csv):
            confirmed_entry = entry[0]
            deaths_entry = entry[1]
            recovered_entry = entry[2]

            province_state = confirmed_entry[0]
            country_region = confirmed_entry[1]
            lat = confirmed_entry[2]
            long = confirmed_entry[3]

            if country_region == "UK":
                country_region = "United Kingdom"

            country_region_short = cc.convert(
                names=[country_region], to="name_short", not_found="n/a"
            )
            iso3 = cc.convert(names=[country_region], to="iso3", not_found=None)

            for i, report_date in enumerate(
                reporting_dates[most_recent_date_index:],
                start=4 + most_recent_date_index,
            ):
                record = GlobalDailyCases(
                    **{
                        "country_region": country_region_short,
                        "province_state": province_state,
                        "lat": lat,
                        "long": long,
                        "date": report_date,
                        "confirmed": confirmed_entry[i],
                        "deaths": deaths_entry[i],
                        "recovered": recovered_entry[i],
                        "iso3": iso3,
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
