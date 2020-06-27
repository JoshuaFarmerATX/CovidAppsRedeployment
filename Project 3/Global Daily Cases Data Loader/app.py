import datetime
import requests
import csv
import pandas as pd
from contextlib import closing
from country_converter import CountryConverter
from flask import Flask, make_response

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from connection import conn_string_proxy, conn_string_deploy

Base = declarative_base()


class GlobalDailyCases(Base):
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


app = Flask(__name__)


@app.route("/")
def load():

    # Connect to the "Covid" database

    # Change connection_string to conn_string_proxy when connecting locally
    # via proxy and to conn_string_deploy when being uploaded for GCP.

    connection_string = conn_string_proxy

    engine = create_engine(connection_string)

    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    ### World Data
    confirmed_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    deaths_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    recovered_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

    confirmed_r = requests.get(confirmed_url, stream=True)
    deaths_r = closing(requests.get(deaths_url, stream=True))
    recovered_r = closing(requests.get(recovered_url, stream=True))

    with closing(requests.get(confirmed_url, stream=True)) as confirmed_r, 
        closing(requests.get(deaths_url, stream=True)) as deaths_r, 
        closing(requests.get(recovered_url, stream=True)) as recovered_r:

        confirmed_csv = csv.reader(confirmed_r.iter_lines(), delimeter=",")
        deaths_csv = csv.reader(deaths_r.iter_lines(), delimeter=",")
        recovered_csv = csv.reader(recovered_r.iter_lines(), delimeter=",")

        csv_headers = list(next(confirmed_csv))
        reporting_dates = headers[4:]

        next(deaths_csv)
        next(recovered_csv)

        cc = CountryConverter()

        for entry in zip(confirmed_csv, deaths_csv, recovered_csv):
            confirmed_entry = entry[0]
            deaths_entry = entry[1]
            recovered_entry = entry[2]

            province_state = confirmed_entry[0]
            country_region = confirmed_entry[1]
            lat = confirmed_entry[2]
            long = confirmed_entry[3]

            country_region = (
                "United Kingdom" if country_region == "UK" else country_region
            )

            for i, report_date in enumerate(reporting_dates, start=4):
                record = GlobalDailyCases(
                    **{
                        "country_region": cc.convert(
                            names=[country_region], to="name_short", not_found="n/a"
                        ),
                        "province_state": province_state,
                        "lat": lat,
                        "long": long,
                        "date": datetime.strptime(report_date, "%m/%d/%y").date(),
                        "confirmed": confirmed_entry[i],
                        "deaths": deaths_entry[i],
                        "recovered": recovered_entry[i],
                        "iso3": cc.convert(
                            names=[country_region], to="iso3", not_found=None
                        ),
                    }
                )
                session.add(record)

    session.commit()

    ###########################################################################
    ############################# Old Below ###################################
    ###########################################################################

    confirmed_html = requests.get(confirmed_url).text
    confirmed_df = pd.read_html(confirmed_html)[0]
    confirmed_df = confirmed_df.iloc[:, 1:]
    confirmed_df = confirmed_df.melt(
        id_vars=["Country/Region", "Province/State", "Lat", "Long"]
    )
    confirmed_df = confirmed_df.rename(
        columns={
            "Country/Region": "country_region",
            "Province/State": "province_state",
            "Lat": "lat",
            "Long": "long",
            "variable": "date",
            "value": "confirmed",
        }
    )

    # Covid-19 Deaths
    deaths_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    deaths_html = requests.get(deaths_url).text
    deaths_df = pd.read_html(deaths_html)[0]
    deaths_df = deaths_df.iloc[:, 1:]
    deaths_df = deaths_df.melt(
        id_vars=["Country/Region", "Province/State", "Lat", "Long"]
    )
    deaths_df = deaths_df.rename(
        columns={
            "Country/Region": "country_region",
            "Province/State": "province_state",
            "Lat": "lat",
            "Long": "long",
            "variable": "date",
            "value": "deaths",
        }
    )

    # Covid-19 Recovered
    recovered_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    recovered_html = requests.get(recovered_url).text
    recovered_df = pd.read_html(recovered_html)[0]
    recovered_df = recovered_df.iloc[:, 1:]
    recovered_df = recovered_df.melt(
        id_vars=["Country/Region", "Province/State", "Lat", "Long"]
    )
    recovered_df = recovered_df.rename(
        columns={
            "Country/Region": "country_region",
            "Province/State": "province_state",
            "Lat": "lat",
            "Long": "long",
            "variable": "date",
            "value": "recovered",
        }
    )

    # Merge three dataframes
    covid_merge1 = pd.merge(confirmed_df, deaths_df, how="outer")
    covid_merge2 = pd.merge(covid_merge1, recovered_df, how="outer")

    # Transform "Date" column into datetime format
    covid_merge2["date"] = pd.to_datetime(covid_merge2["date"])
    covid_merge2["date"] = covid_merge2["date"].dt.date

    # Change "UK" for "United Kingdom"
    covid_merge2 = covid_merge2.replace(to_replace="UK", value="United Kingdom")

    # Add column ISO3 to "covid_merge2"
    some_names_confirmed = list(covid_merge2.country_region)
    standard_names = coco.convert(
        names=some_names_confirmed, to="name_short", not_found="n/a"
    )
    iso3_codes = coco.convert(names=standard_names, to="iso3", not_found=None)
    covid_merge2["iso3"] = iso3_codes
    covid_df = covid_merge2

    # Create a customized dataframe for Sinah's plots
    ### Add column ISO3 to "covid_df"
    iso_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv"
    iso_html = requests.get(iso_url).text
    iso_df = pd.read_html(iso_html)[0]
    iso3_df = iso_df[["iso3", "Country_Region", "Province_State"]].rename(
        columns={"Country_Region": "country_region", "Province_State": "province_state"}
    )
    iso3_df = iso3_df.loc[iso3_df["province_state"].isnull()].drop("province_state", 1)
    old_pop_df = pd.read_csv("older_pop_2018.csv")

    covid_df2 = covid_df[
        ["country_region", "date", "province_state", "confirmed", "deaths", "recovered"]
    ]
    covid_df2 = covid_df2.groupby(["country_region", "date"]).sum().reset_index()
    covid_df2["case_fatality"] = round(
        covid_df2["deaths"] / covid_df2["confirmed"] * 100, 2
    )
    covid_df3 = pd.merge(covid_df2, iso3_df, how="left")
    plot_df = pd.merge(covid_df3, old_pop_df, how="left")
    plot_df = (
        plot_df.loc[plot_df["date"] >= datetime.date(2020, 3, 1)]
        .reset_index()
        .drop("index", axis=1)
    )

    # Connect to the "Covid" database

    # Change connection_string to conn_string_proxy when connecting locally
    # via proxy and to conn_string_deploy when being uploaded for GCP.

    connection_string = conn_string_proxy

    engine = create_engine(connection_string)

    Base.metadata.create_all(engine)

    session = Session(bin=engine)

    # Create "daily_cases" table in "Covid" database with "covid_db" dataframe
    covid_merge2.to_sql(con=engine, name="daily_cases", if_exists="replace")
    plot_df.to_sql(con=engine, name="plotting", if_exists="replace")

    return make_response("Successful", 200)


if __name__ == "__main__":
    app.run()
