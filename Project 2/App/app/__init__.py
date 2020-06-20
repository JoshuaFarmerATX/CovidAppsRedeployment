import sqlalchemy
from typing import List

from flask import Flask, _app_ctx_stack, jsonify, url_for, render_template, request
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from sqlalchemy import (
    func,
    MetaData,
    desc,
    Column,
    Integer,
    String,
    DateTime,
    table,
    Date,
    create_engine,
    inspect,
)

from . import models
from .database import SessionLocal, engine
from .plot import bar_fig, bubble_fig
from .map_plots import create_map

import json

import datetime

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/")
def home():

    dateUpdated = json.loads(globaltotals())[0].get("Last Update")
    deaths = json.loads(globaltotals())[0].get("Deaths")
    cases = json.loads(globaltotals())[0].get("Cases")
    recovered = json.loads(globaltotals())[0].get("Recovered")
    case_fatality = round(deaths / cases * 100, 2)
    return render_template(
        "index.html",
        bar=bar_fig(),
        deaths=deaths,
        cases=cases,
        recovered=recovered,
        dateUpdated=dateUpdated,
        case_fatality=case_fatality,
    )


@app.route("/routes")
def routes():
    return render_template("routes.html")


@app.route("/team")
def team():
    return render_template("team.html")


# API Route 1: Most Recent Totals for Every Country Worldwide
@app.route("/API/most_recent/")
def worldwidetotals():
    subquery1 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwidetotals = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(models.Cases.date.in_(subquery1))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict = []
    for item in worldwidetotals:
        dict.append(
            {
                "ISO3": item[5],
                "Country": item[0],
                "Last Update": str(item[1]),
                "Cases": int(item[2]),
                "Deaths": int(item[3]),
                "Recovered": int(item[4]),
            }
        )
    dicts = json.dumps(dict)
    return dicts


# API Route 2: Most Recent Confirmed Cases for Every Country Worldwide


@app.route("/API/cases/")
def worldwidecases():
    subquery2 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwidecases = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            models.Cases.iso3,
        )
        .filter(models.Cases.date.in_(subquery2))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict2 = []
    for item in worldwidecases:
        dict2.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Cases": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts2 = json.dumps(dict2)
    return dicts2


# API Route 3: Most Recent Deaths for Every Country Worldwide


@app.route("/API/dead/")
def worldwidedead():
    subquery3 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwidedead = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.deaths),
            models.Cases.iso3,
        )
        .filter(models.Cases.date.in_(subquery3))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict3 = []
    for item in worldwidedead:
        dict3.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Deaths": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts3 = json.dumps(dict3)
    return dicts3


# API Route 4: Most Recent Number of Recoveries for Every Country Worldwide


@app.route("/API/recovered/")
def worldwiderecovered():
    subquery4 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwiderecovered = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(models.Cases.date.in_(subquery4))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict4 = []
    for item in worldwiderecovered:
        dict4.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Recovered": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts4 = json.dumps(dict4)
    return dicts4


# API Route 5: Most Recent Totals by Country


@app.route("/API/<iso3>/")
def countrytotals(iso3):
    subquery5 = app.session.query(func.max(models.Cases.date)).subquery()
    countrytotals = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery5))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict5 = []
    for item in countrytotals:
        dict5.append(
            {
                "ISO3": item[5],
                "Country": item[0],
                "Last Update": str(item[1]),
                "Cases": int(item[2]),
                "Deaths": int(item[3]),
                "Recovered": int(item[4]),
            }
        )
    dicts5 = json.dumps(dict5)
    return dicts5


# API Route 6: Most Recent Cases by Country


@app.route("/API/cases/<iso3>/")
def countrycases(iso3):
    subquery6 = app.session.query(func.max(models.Cases.date)).subquery()
    countrycases = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery6))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict6 = []
    for item in countrycases:
        dict6.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Cases": int(item[2]),
                "Last Updated": str(item[1]),
            }
        )
    dicts6 = json.dumps(dict6)
    return dicts6


# API Route 7: Most Recent Dead by Country


@app.route("/API/dead/<iso3>/")
def countrydead(iso3):
    subquery7 = app.session.query(func.max(models.Cases.date)).subquery()
    countrydead = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.deaths),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery7))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict7 = []
    for item in countrydead:
        dict7.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Deaths": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts7 = json.dumps(dict7)
    return dicts7


# API Route 8: Most Recent Recovered by Country


@app.route("/API/recovered/<iso3>/")
def countryrecovered(iso3):
    subquery8 = app.session.query(func.max(models.Cases.date)).subquery()
    countryrecovered = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery8))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict8 = []
    for item in countryrecovered:
        dict8.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Recovered": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts8 = json.dumps(dict8)
    return dicts8


# API Route 9: Country Timeseries


@app.route("/API/<iso3>/timeseries/")
def countrytimeseries(iso3):
    countrytimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .group_by(models.Cases.date)
        .all()
    )
    dict9 = []
    for item in countrytimeseries:
        dict9.append(
            {
                "ISO3": item[5],
                "Country": item[0],
                "Total Results as of Date": str(item[1]),
                "Cases": int(item[2]),
                "Deaths": int(item[3]),
                "Recovered": int(item[4]),
            }
        )
    dicts9 = json.dumps(dict9)
    return dicts9


# API Route 10: Global Timeseries


@app.route("/API/timeseries/")
def globaltimeseries():
    globaltimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .group_by(models.Cases.date)
        .all()
    )
    dict10 = []
    for item in globaltimeseries:
        dict10.append(
            {
                "Total Results as of Date": str(item[1]),
                "Cases": int(item[2]),
                "Deaths": int(item[3]),
                "Recovered": int(item[4]),
            }
        )
    dicts10 = json.dumps(dict10)
    return dicts10


# API Route 11: Global Timeseries for Cases


@app.route("/API/cases/timeseries/")
def casestimeseries():
    casestimeseries = (
        app.session.query(models.Cases.date, func.sum(models.Cases.confirmed),)
        .group_by(models.Cases.date)
        .all()
    )
    dict11 = []
    for item in casestimeseries:
        dict11.append(
            {"Total Results as of Date": str(item[0]), "Cases": int(item[1]),}
        )
    dicts11 = json.dumps(dict11)
    return dicts11


# API Route 12: Global Timeseries for Deaths
@app.route("/API/dead/timeseries/")
def deadtimeseries():
    deadtimeseries = (
        app.session.query(models.Cases.date, func.sum(models.Cases.deaths),)
        .group_by(models.Cases.date)
        .all()
    )
    dict12 = []
    for item in deadtimeseries:
        dict12.append(
            {"Total Results as of Date": str(item[0]), "Deaths": int(item[1]),}
        )
    dicts12 = json.dumps(dict12)
    return dicts12


# API Route 13: Global Timeseries for Recoveries
@app.route("/API/recovered/timeseries/")
def recoveredtimeseries():
    recoveredtimeseries = (
        app.session.query(models.Cases.date, func.sum(models.Cases.recovered),)
        .group_by(models.Cases.date)
        .all()
    )
    dict13 = []
    for item in recoveredtimeseries:
        dict13.append(
            {"Total Results as of Date": str(item[0]), "Recovered": int(item[1]),}
        )
    dicts13 = json.dumps(dict13)
    return dicts13


# API Route 14: Country Timeseries for Cases


@app.route("/API/cases/<iso3>/timeseries/")
def countrycasestimeseries(iso3):
    countrycasestimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .group_by(models.Cases.date)
        .all()
    )
    dict14 = []
    for item in countrycasestimeseries:
        dict14.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Total Results as of Date": str(item[1]),
                "Cases": int(item[2]),
            }
        )
    dicts14 = json.dumps(dict14)
    return dicts14


# API Route 15: Country Timeseries for Deaths
@app.route("/API/dead/<iso3>/timeseries/")
def countrydeadtimeseries(iso3):
    countrydeadtimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.deaths),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .group_by(models.Cases.date)
        .all()
    )
    dict15 = []
    for item in countrydeadtimeseries:
        dict15.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Total Results as of Date": str(item[1]),
                "Deaths": int(item[2]),
            }
        )
    dicts15 = json.dumps(dict15)
    return dicts15


# API Route 16: Country Timeseries for Recoveries
@app.route("/API/recovered/<iso3>/timeseries/")
def countryrecoveredtimeseries(iso3):
    countryrecoveredtimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .group_by(models.Cases.date)
        .all()
    )
    dict16 = []
    for item in countryrecoveredtimeseries:
        dict16.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Total Results as of Date": str(item[1]),
                "Recovered": int(item[2]),
            }
        )
    dicts16 = json.dumps(dict16)
    return dicts16


# API Route 17: Totals for Every Country Worldwide as of Particular Date
@app.route("/API/bydate/<asof>/")
def worldwidetotalsdate(asof):
    worldwidetotalsdate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict17 = []
    for item in worldwidetotalsdate:
        dict17.append(
            {
                "ISO3": item[5],
                "Country": item[0],
                "Date": str(item[1]),
                "Cases": int(item[2]),
                "Deaths": int(item[3]),
                "Recovered": int(item[4]),
            }
        )
    dicts17 = json.dumps(dict17)
    return dicts17


# API Route 18: Confirmed Cases for Every Country Worldwide as of Particular Date


@app.route("/API/cases/bydate/<asof>/")
def worldwidecasesdate(asof):
    worldwidecasesdate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            models.Cases.iso3,
        )
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict18 = []
    for item in worldwidecasesdate:
        dict18.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Cases": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts18 = json.dumps(dict18)
    return dicts18


# API Route 19: Deaths for Every Country Worldwide as of Particular Date


@app.route("/API/dead/bydate/<asof>/")
def worldwidedeaddate(asof):
    worldwidedeaddate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.deaths),
            models.Cases.iso3,
        )
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict19 = []
    for item in worldwidedeaddate:
        dict19.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Deaths": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts19 = json.dumps(dict19)
    return dicts19


# API Route 20: Recoveries for Every Country Worldwide as of Particular Date


@app.route("/API/recovered/bydate/<asof>/")
def worldwiderecovereddate(asof):
    worldwiderecovereddate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict20 = []
    for item in worldwiderecovereddate:
        dict20.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Recovered": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts20 = json.dumps(dict20)
    return dicts20


# API Route 21: Totals by Country as of Particular Date


@app.route("/API/<iso3>/bydate/<asof>/")
def countrytotalsdate(iso3, asof):
    countrytotalsdate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict21 = []
    for item in countrytotalsdate:
        dict21.append(
            {
                "ISO3": item[5],
                "Country": item[0],
                "Last Update": str(item[1]),
                "Cases": int(item[2]),
                "Deaths": int(item[3]),
                "Recovered": int(item[4]),
            }
        )
    dicts21 = json.dumps(dict21)
    return dicts21


# API Route 22: Cases by Country as of Particular Date


@app.route("/API/cases/<iso3>/bydate/<asof>/")
def countrycasesdate(iso3, asof):
    countrycasesdate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict22 = []
    for item in countrycasesdate:
        dict22.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Cases": int(item[2]),
                "Last Updated": str(item[1]),
            }
        )
    dicts22 = json.dumps(dict22)
    return dicts22


# API Route 23: Dead by Country as of Particular Date


@app.route("/API/dead/<iso3>/bydate/<asof>/")
def countrydeaddate(iso3, asof):
    countrydeaddate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.deaths),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict23 = []
    for item in countrydeaddate:
        dict23.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Deaths": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts23 = json.dumps(dict23)
    return dicts23


# API Route 24: Recovered by Country as of Particular Date


@app.route("/API/recovered/<iso3>/bydate/<asof>/")
def countryrecovereddate(iso3, asof):
    countryrecovereddate = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.recovered),
            models.Cases.iso3,
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .group_by(models.Cases.iso3)
        .all()
    )
    dict24 = []
    for item in countryrecovereddate:
        dict24.append(
            {
                "ISO3": item[3],
                "Country": item[0],
                "Recovered": int(item[2]),
                "Last Update": str(item[1]),
            }
        )
    dicts24 = json.dumps(dict24)
    return dicts24


# API Route 25: Most Recent Totals Globally (sum)
@app.route("/API/global/most_recent/")
def globaltotals():
    subquery25 = app.session.query(func.max(models.Cases.date)).subquery()
    globaltotals = (
        app.session.query(
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(models.Cases.date.in_(subquery25))
        .all()
    )
    dict25 = []
    for item in globaltotals:
        dict25.append(
            {
                "Last Update": str(item[0]),
                "Cases": int(item[1]),
                "Deaths": int(item[2]),
                "Recovered": int(item[3]),
            }
        )
    dicts25 = json.dumps(dict25)
    return dicts25


# API Route 26: Most Recent Confirmed Cases Globally (sum)


@app.route("/API/global/cases/")
def globalcases():
    subquery26 = app.session.query(func.max(models.Cases.date)).subquery()
    globalcases = (
        app.session.query(models.Cases.date, func.sum(models.Cases.confirmed),)
        .filter(models.Cases.date.in_(subquery26))
        .all()
    )
    dict26 = []
    for item in globalcases:
        dict26.append({"Cases": int(item[1]), "Last Update": str(item[0])})
    dicts26 = json.dumps(dict26)
    return dicts26


# API Route 27: Most Recent Deaths Globally (sum)


@app.route("/API/global/dead/")
def globaldead():
    subquery27 = app.session.query(func.max(models.Cases.date)).subquery()
    globaldead = (
        app.session.query(models.Cases.date, func.sum(models.Cases.deaths),)
        .filter(models.Cases.date.in_(subquery27))
        .all()
    )
    dict27 = []
    for item in globaldead:
        dict27.append({"Deaths": int(item[1]), "Last Update": str(item[0])})
    dicts27 = json.dumps(dict27)
    return dicts27


# API Route 28: Most Recent Number of Recoveries Globally (sum)


@app.route("/API/global/recovered/")
def globalcovered():
    subquery28 = app.session.query(func.max(models.Cases.date)).subquery()
    globalrecovered = (
        app.session.query(models.Cases.date, func.sum(models.Cases.recovered),)
        .filter(models.Cases.date.in_(subquery28))
        .all()
    )
    dict28 = []
    for item in globalrecovered:
        dict28.append({"Recovered": int(item[1]), "Last Update": str(item[0])})
    dicts28 = json.dumps(dict28)
    return dicts28


# API Route 29: Totals Globally (sum) as of Particular Date


@app.route("/API/global/bydate/<asof>/")
def globallytotalsdate(asof):
    globallytotalsdate = (
        app.session.query(
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .all()
    )
    dict29 = []
    for item in globallytotalsdate:
        dict29.append(
            {
                "Last Update": str(item[0]),
                "Cases": int(item[1]),
                "Deaths": int(item[2]),
                "Recovered": int(item[3]),
            }
        )
    dicts29 = json.dumps(dict29)
    return dicts29


# API Route 30: Cases Globally (sum) as of Particular Date


@app.route("/API/cases/global/bydate/<asof>/")
def globallycasesdate(asof):
    globallycasesdate = (
        app.session.query(models.Cases.date, func.sum(models.Cases.confirmed),)
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .all()
    )
    dict30 = []
    for item in globallycasesdate:
        dict30.append({"Cases": int(item[1]), "Last Updated": str(item[0])})
    dicts30 = json.dumps(dict30)
    return dicts30


# API Route 31: Dead Globally (sum) as of Particular Date


@app.route("/API/dead/global/bydate/<asof>/")
def globallydeaddate(asof):
    globallydeaddate = (
        app.session.query(models.Cases.date, func.sum(models.Cases.deaths),)
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .all()
    )
    dict31 = []
    for item in globallydeaddate:
        dict31.append({"Deaths": int(item[1]), "Last Update": str(item[0])})
    dicts31 = json.dumps(dict31)
    return dicts31


# API Route 32: Recovered Globally (sum) as of Particular Date


@app.route("/API/recovered/global/bydate/<asof>/")
def globallyrecovereddate(asof):
    globallyrecovereddate = (
        app.session.query(models.Cases.date, func.sum(models.Cases.recovered),)
        .filter(datetime.datetime.strptime(asof, "%Y-%m-%d") == models.Cases.date)
        .all()
    )
    dict32 = []
    for item in globallyrecovereddate:
        dict32.append(
            {"Recovered": int(item[1]), "Last Update": str(item[0]),}
        )
    dicts32 = json.dumps(dict32)
    return dicts32


# All records (from Daniela)
@app.route("/records/")
def show_records():
    cases = app.session.query(models.Cases).all()
    return jsonify([record.to_dict() for record in records])


# All cases by date by country (from Daniela).
@app.route("/country/<iso3>")
def country_by_ISO3(iso3):
    try:
        country = app.session.query(models.Record).filter_by(iso3=iso3).all()
        return jsonify([record.to_dict() for record in country])
    except:
        return jsonify()


# World cases (from Daniela)
@app.route("/total_world")
def total_world():
    totals = app.session.query(models.WorldTotalRecords).all()
    return jsonify([record.to_dict() for record in totals])


@app.route("/map")
def map():
    return render_template(
        "map.html",
        confirmed=create_map("confirmed"),
        deaths=create_map("deaths"),
        recovered=create_map("recovered"),
    )


@app.route("/plot")
def render_plots():
    return render_template("plot.html", bubble=bubble_fig())


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


if __name__ == "__main__":
    app.run()
