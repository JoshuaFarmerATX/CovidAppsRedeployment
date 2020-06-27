import pymysql
from collections import OrderedDict
from pymysql.cursors import DictCursorMixin, Cursor
from pprint import pprint
from fastapi import FastAPI
import uvicorn
from connection import conn_string_deploy

# Change mydb to conn_string_proxy when connecting locally
# via proxy and to conn_string_deploy when being uploaded for GCP.

mydb = conn_string_deploy


class OrderedDictCursor(DictCursorMixin, Cursor):
    dict_type = OrderedDict


cursor = mydb.cursor(OrderedDictCursor)

app = FastAPI()


@app.get("/")
def home():
    return "API Access OK"


# API Route 1: Most Recent Totals for Every Country Worldwide
@app.get("/API/most_recent", tags=["Global Most Recent"])
async def most_recent_totals_for_all_countries():
    cursor.execute(
        "SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases)"
    )
    return cursor.fetchall()


# API Route 2: Most Recent Confirmed Cases for Every Country Worldwide
@app.get("/API/most_recent/cases", tags=["Global Most Recent"])
async def most_recent_cases_for_all_countries():
    cursor.execute(
        "SELECT iso3 AS ISO3, country_region AS Country, confirmed AS Cases, date AS 'Last Update' FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases)"
    )
    return cursor.fetchall()


# API Route 3: Most Recent Deaths for Every Country Worldwide
@app.get("/API/most_recent/deaths", tags=["Global Most Recent"])
async def most_recent_deaths_for_all_countries():
    cursor.execute(
        "SELECT iso3 AS ISO3, country_region AS Country, deaths AS Deaths, date AS 'Last Update' FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases)"
    )
    return cursor.fetchall()


# API Route 4: Most Recent Number of Recoveries for Every Country Worldwide
@app.get("/API/most_recent/recovered", tags=["Global Most Recent"])
async def most_recent_recovered_for_all_countries():
    cursor.execute(
        "SELECT iso3 AS ISO3, country_region AS Country, recovered AS Recovered, date AS 'Last Update' FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases)"
    )
    return cursor.fetchall()


# API Route 5: Most Recent Totals by Country
@app.get("/API/most_recent/{iso3_code}", tags=["Global Most Recent"])
async def most_recent_totals_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) AND iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 6: Most Recent Cases by Country
@app.get("/API/most_recent/cases/{iso3_code}", tags=["Global Most Recent"])
async def most_recent_cases_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, confirmed AS Cases, date AS 'Last Update' FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) AND iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 7: Most Recent Dead by Country
@app.get("/API/most_recent/dead/{iso3_code}", tags=["Global Most Recent"])
async def most_recent_dead_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, deaths AS Deaths, date AS 'Last Update' FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) AND iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 8: Most Recent Recovered by Country
@app.get("/API/most_recent/recovered/{iso3_code}", tags=["Global Most Recent"])
async def most_recent_recovered_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, recovered AS Recovered, date AS 'Last Update' FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) AND iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 9: Global Timeseries
@app.get("/API/timeseries", tags=["Global Time Series"])
async def global_time_series():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM daily_cases GROUP BY date"
    )
    return cursor.fetchall()


# API Route 10: Global TImeseries for Cases
@app.get("/API/timeseries/cases", tags=["Global Time Series"])
async def global_time_series_for_number_of_cases():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases FROM daily_cases GROUP BY date"
    )
    return cursor.fetchall()


# API Route 11: Global TImeseries for Deaths
@app.get("/API/timeseries/deaths", tags=["Global Time Series"])
async def global_timeseries__for_number_of_deaths():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(deaths) AS Deaths FROM daily_cases GROUP BY date"
    )
    return cursor.fetchall()


# API Route 12: Global TImeseries for Recovered
@app.get("/API/timeseries/recovered", tags=["Global Time Series"])
async def global_timeseries_for_number_of_recoveries():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(recovered) AS Recovered FROM daily_cases GROUP BY date"
    )
    return cursor.fetchall()


# API Route 13: Timeseries by Country
@app.get("/API/timeseries/{iso3_code}", tags=["Global Time Series"])
async def timeseries_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Totals as of Date', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM daily_cases WHERE iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 14: Timeseries of Cases by Country
@app.get("/API/timeseries/cases/{iso3_code}", tags=["Global Time Series"])
async def timeseries_of_cases_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Total Results as of Date', confirmed AS Cases FROM daily_cases WHERE iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 15: Timeseries of Deaths by Country
@app.get("/API/timeseries/deaths/{iso3_code}", tags=["Global Time Series"])
async def timeseries_of_deaths_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Total Results as of Date', deaths AS Deaths FROM daily_cases WHERE iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 16: Timeseries of Deaths by Country
@app.get("/API/timeseries/recovered/{iso3_code}", tags=["Global Time Series"])
async def timeseries_of_recovered_by_country_selection_using_iso3_code(iso3_code):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date as 'Total Results as of Date', recovered AS Recovered FROM daily_cases WHERE iso3 = '{iso3_code}'"
    )
    return cursor.fetchall()


# API Route 17: Totals for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/{asof_date}", tags=["Global By Date"])
async def totals_for_every_country_as_of_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT date AS 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 18: Confirmed Cases for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/cases/{asof_date}", tags=["Global By Date"])
async def cases_for_every_country_as_of_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT date AS 'Total Results as of Date', SUM(confirmed) AS Cases FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 19: Deaths for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/deaths/{asof_date}", tags=["Global By Date"])
async def deaths_for_every_country_as_of_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT date AS 'Total Results as of Date', SUM(deaths) AS Deaths FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 20: Recovered for Every Country Worldwide as of Particular Date
@app.get("/API/bydate/recovered/{asof_date}", tags=["Global By Date"])
async def recoveries_for_every_country_as_of_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT date AS 'Total Results as of Date', SUM(recovered) AS Recovered FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 21: Specific Country Totals as of a particular date
@app.get("/API/bydate/countrytotals/{iso3_code}/{asof_date}", tags=["Global By Date"])
async def specific_country_totals_as_of_a_specific_date_using_iso3_code_for_country_and_date_formatted_YYYYMMDD(
    iso3_code, asof_date
):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths, recovered AS Recovered FROM daily_cases WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'"
    )
    return cursor.fetchall()


# API Route 22: Specific Country Cases as of a particular date
@app.get("/API/bydate/countrycases/{iso3_code}/{asof_date}", tags=["Global By Date"])
async def specific_country_cases_as_of_a_specific_date_using_iso3_code_for_country_and_date_formatted_YYYYMMDD(
    iso3_code, asof_date
):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', confirmed AS Cases FROM daily_cases WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'"
    )
    return cursor.fetchall()


# API Route 23: Specific Country Deaths as of a particular date
@app.get("/API/bydate/countrydeaths/{iso3_code}/{asof_date}", tags=["Global By Date"])
async def specific_country_deaths_as_of_a_specific_date_using_iso3_code_for_country_and_date_formatted_YYYYMMDD(
    iso3_code, asof_date
):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', deaths AS Deaths FROM daily_cases WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'"
    )
    return cursor.fetchall()


# API Route 24: Specific Country Recoveries as of a particular date
@app.get(
    "/API/bydate/countryrecoveries/{iso3_code}/{asof_date}", tags=["Global By Date"]
)
async def specific_country_recoveries_as_of_a_specific_date_using_iso3_code_for_country_and_date_formatted_YYYYMMDD(
    iso3_code, asof_date
):
    cursor.execute(
        f"SELECT iso3 AS ISO3, country_region AS Country, date AS 'Last Update', recovered AS Recovered FROM daily_cases WHERE iso3 = '{iso3_code}' AND date = '{asof_date}'"
    )
    return cursor.fetchall()


# API Route 25: Most Recent Worldwide Totals
@app.get("/API/global_totals/most_recent", tags=["Global Most Recent"])
async def most_recent_global_totals():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) GROUP BY date"
    )
    return cursor.fetchall()


# API Route 26: Most Recent Worldwide Total Cases
@app.get("/API/global_totals/cases/most_recent", tags=["Global Most Recent"])
async def most_recent_global_total_cases():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) GROUP BY date"
    )
    return cursor.fetchall()


# API Route 27: Most Recent Worldwide Total Deaths
@app.get("/API/global_totals/deaths/most_recent", tags=["Global Most Recent"])
async def most_recent_global_total_deaths():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(deaths) AS Deaths FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) GROUP BY date"
    )
    return cursor.fetchall()


# API Route 28: Most Recent Worldwide Total Recovered
@app.get("/API/global_totals/recovered/most_recent", tags=["Global Most Recent"])
async def most_recent_global_total_recoveries():
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(recovered) AS Recovered FROM daily_cases WHERE date = (SELECT MAX(date) FROM daily_cases) GROUP BY date"
    )
    return cursor.fetchall()


# API Route 29: Worldwide Totals as of a specific date
@app.get("/API/global_totals_bydate/{asof_date}", tags=["Global By Date"])
async def global_totals_as_of_a_specific_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths, SUM(recovered) AS Recovered FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 30: Worldwide Total Cases as of a specific date
@app.get("/API/global_total_cases_bydate/{asof_date}", tags=["Global By Date"])
async def global_total_cases_as_of_a_specific_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(confirmed) AS Cases FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 31: Worldwide Total Deaths as of a specific date
@app.get("/API/global_total_deaths_bydate/{asof_date}", tags=["Global By Date"])
async def global_total_deaths_as_of_a_specific_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(deaths) AS Deaths FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 32: Worldwide Total Recovered as of a specific date
@app.get("/API/global_total_recovered_bydate/{asof_date}", tags=["Global By Date"])
async def global_total_recovered_as_of_a_specific_date_formatted_YYYYMMDD(asof_date):
    cursor.execute(
        f"SELECT MAX(date) 'Total Results as of Date', SUM(recovered) AS Recovered FROM daily_cases WHERE date = '{asof_date}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 33: Most Recent Totals for Every State
@app.get("/API/us/most_recent", tags=["USA/States Most Recent"])
async def most_recent_totals_for_every_state():
    cursor.execute(
        "SELECT province_state AS 'State', date AS 'Last Update', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM usa_covid19) GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 34: Most Recent Confirmed Cases for Every State
@app.get("/API/us/most_recent/cases", tags=["USA/States Most Recent"])
async def most_recent_cases_for_every_state():
    cursor.execute(
        "SELECT province_state AS State, date AS 'Last Update', SUM(confirmed) AS Cases FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM usa_covid19) GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 35: Most Recent Deaths for Every State
@app.get("/API/us/most_recent/deaths", tags=["USA/States Most Recent"])
async def most_recent_deaths_for_every_state():
    cursor.execute(
        "SELECT province_state AS State, date AS 'Last Update', SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM usa_covid19) GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 36: Most Recent Totals by State
@app.get("/API/us/most_recent/{state}", tags=["USA/States Most Recent"])
async def most_recent_totals_by_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Last Update', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 37: Most Recent Cases by State
@app.get("/API/us/most_recent/cases/{state}", tags=["USA/States Most Recent"])
async def most_recent_cases_by_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Last Update', SUM(confirmed) AS Cases FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 38: Most Recent Dead by State
@app.get("/API/us/most_recent/dead/{state}", tags=["USA/States Most Recent"])
async def most_recent_dead_by_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Last Update', SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 39: Most Recent Totals by State and All Counties
@app.get("/API/us/{state}/allcounties", tags=["USA/States Most Recent"])
async def most_recent_totals_for_all_counties_in_a_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}'"
    )
    return cursor.fetchall()


# API Route 40: Most Recent Cases by State and All Counties
@app.get("/API/us/cases/{state}/allcounties", tags=["USA/States Most Recent"])
async def most_recent_cases_for_all_counties_in_a_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Last Update', confirmed AS Cases FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}'"
    )
    return cursor.fetchall()


# API Route 41: Most Recent Dead by State and All Counties
@app.get("/API/us/dead/{state}/allcounties", tags=["USA/States Most Recent"])
async def most_recent_deaths_for_all_counties_in_a_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Last Update', deaths AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}'"
    )
    return cursor.fetchall()


# API Route 42: Most Recent Totals by State and Specific Counties
@app.get("/API/us/{state}/{county}", tags=["USA/States Most Recent"])
async def most_recent_totals_by_a_specific_county_in_a_specific_state(state, county):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Last Update', confirmed AS Cases, deaths AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}' and county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 43: Most Recent Cases by State and Specific Counties
@app.get("/API/us/cases/{state}/{county}", tags=["USA/States Most Recent"])
async def most_recent_cases_by_a_specific_county_in_a_specific_state(state, county):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Last Update', confirmed AS Cases FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}' and county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 44: Most Recent Dead by State and Specific Counties
@app.get("/API/us/dead/{state}/{county}", tags=["USA/States Most Recent"])
async def most_recent_dead_by_a_specific_county_in_a_specific_state(state, county):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Last Update', deaths AS Deaths FROM usa_covid19 WHERE date = (SELECT MAX(date) FROM daily_cases) and province_state = '{state}' and county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 45: Timeseries by State
@app.get("/API/us/timeseries/totals/{state}", tags=["USA/States Time Series"])
async def timeseries_by_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Totals as of Date', SUM(confirmed) AS Cases, sum(deaths) AS Deaths FROM usa_covid19 WHERE province_state = '{state}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 46: Timeseries of Cases by State
@app.get("/API/us/timeseries/cases/{state}", tags=["USA/States Time Series"])
async def timeseries_of_cases_by_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Totals as of Date', SUM(confirmed) AS Cases FROM usa_covid19 WHERE province_state = '{state}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 47: Timeseries of Deaths by State
@app.get("/API/us/timeseries/dead/{state}", tags=["USA/States Time Series"])
async def timeseries_of_deaths_by_specific_state(state):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Totals as of Date', sum(deaths) AS Deaths FROM usa_covid19 WHERE province_state = '{state}' GROUP BY date"
    )
    return cursor.fetchall()


# API Route 48: Timeseries by State and All Counties
@app.get("/API/us/timeseries/{state}/allcounties", tags=["USA/States Time Series"])
async def timeseries_of_totals_for_all_counties_in_a_specific_state_ordered_by_county(
    state,
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases, deaths AS Deaths FROM usa_covid19 WHERE province_state = '{state}' ORDER BY county_city"
    )
    return cursor.fetchall()


# API Route 49: Timeseries of Cases by State and All Counties
@app.get(
    "/API/us/timeseries/cases/{state}/allcounties", tags=["USA/States Time Series"]
)
async def timeseries_of_cases_for_all_counties_in_a_specific_state_ordered_by_county(
    state,
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases FROM usa_covid19 WHERE province_state = '{state}' ORDER BY county_city"
    )
    return cursor.fetchall()


# API Route 50: Timeseries of Deaths by State and All Counties
@app.get(
    "/API/us/timeseries/deaths/{state}/allcounties", tags=["USA/States Time Series"]
)
async def timeseries_of_deaths_for_all_counties_in_a_specific_state_ordered_by_county(
    state,
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', deaths AS Deaths FROM usa_covid19 WHERE province_state = '{state}' ORDER BY county_city"
    )
    return cursor.fetchall()


# API Route 51: Timeseries by State and Specific Counties
@app.get("/API/us/timeseries/{state}/{county}", tags=["USA/States Time Series"])
async def timeseries_of_totals_by_specific_state_and_county(state, county):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases, deaths AS Deaths FROM usa_covid19 WHERE province_state = '{state}' AND county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 52: Timeseries of Cases by State and Specific Counties
@app.get("/API/us/timeseries/cases/{state}/{county}", tags=["USA/States Time Series"])
async def timeseries_of_cases_by_specific_state_and_county(state, county):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases FROM usa_covid19 WHERE province_state = '{state}' AND county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 53: Timeseries of Deaths by State and Specific Counties
@app.get("/API/us/timeseries/deaths/{state}/{county}", tags=["USA/States Time Series"])
async def timeseries_of_deaths_by_specific_state_and_county(state, county):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', deaths AS Deaths FROM usa_covid19 WHERE province_state = '{state}' AND county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 54: Totals for Every State by Date
@app.get("/API/us/totals/bydate/{date}", tags=["USA/States by Date"])
async def totals_for_all_states_as_of_a_specific_date_formatted_YYYYMMDD(date):
    cursor.execute(
        f"SELECT province_state AS 'State', date AS 'Totals as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = '{date}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 55: Confirmed Cases for Every State by Date
@app.get("/API/us/{date}/cases/", tags=["USA/States by Date"])
async def cases_for_all_states_as_of_a_specific_date_formatted_YYYYMMDD(date):
    cursor.execute(
        f"SELECT province_state AS 'State', date AS 'Totals as of Date', SUM(confirmed) AS Cases FROM usa_covid19 WHERE date = '{date}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 56: Deaths for Every State by Date
@app.get("/API/us/bydate/{date}/deaths", tags=["USA/States by Date"])
async def deaths_for_all_states_as_of_a_specific_date_formatted_YYYYMMDD(date):
    cursor.execute(
        f"SELECT province_state AS 'State', date AS 'Totals as of Date', SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = '{date}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 57: Totals by State by Date
@app.get("/API/us/totals/{date}/{state}", tags=["USA/States by Date"])
async def totals_by_specific_state_and_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state
):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Totals as of Date', SUM(confirmed) AS Cases, SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 58: Cases by State by Date
@app.get("/API/us/{date}/cases/{state}", tags=["USA/States by Date"])
async def cases_by_specific_state_and_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state
):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Totals as of Date', SUM(confirmed) AS Cases FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 59: Dead by State by Date
@app.get("/API/us/{date}/dead/{state}", tags=["USA/States by Date"])
async def deaths_by_specific_state_and_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state
):
    cursor.execute(
        f"SELECT province_state AS State, date AS 'Totals as of Date', SUM(deaths) AS Deaths FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}' GROUP BY province_state"
    )
    return cursor.fetchall()


# API Route 60: Totals by State and All Counties by Date
@app.get("/API/us/{date}/{state}/allcounties", tags=["USA/States by Date"])
async def totals_for_all_counties_in_a_specific_state_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases, deaths AS Deaths FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}'"
    )
    return cursor.fetchall()


# API Route 61: Cases by State and All Counties By Date
@app.get("/API/us/cases/{date}/cases/{state}/allcounties", tags=["USA/States by Date"])
async def cases_for_all_counties_in_a_specific_state_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}'"
    )
    return cursor.fetchall()


# API Route 62: Dead by State and All Counties by Date
@app.get("/API/us/{date}/dead/{state}/allcounties", tags=["USA/States by Date"])
async def deaths_for_all_counties_in_a_specific_state_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', deaths AS Deaths FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}'"
    )
    return cursor.fetchall()


# API Route 63: Totals by Date, State and Specific Counties
@app.get("/API/us/{date}/{state}/{county}", tags=["USA/States by Date"])
async def totals_for_a_specific_county_in_a_specific_state_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state, county
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases, deaths AS Deaths FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}' and county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 64: Cases by Date, State and Specific Counties
@app.get("/API/us/cases/{date}/{state}/{county}", tags=["USA/States by Date"])
async def cases_for_a_specific_county_in_a_specific_state_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state, county
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', confirmed AS Cases FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}' and county_city = '{county}'"
    )
    return cursor.fetchall()


# API Route 65: Dead by Date, State and Specific Counties
@app.get("/API/us/dead/{date}/{state}/{county}", tags=["USA/States by Date"])
async def deaths_for_a_specific_county_in_a_specific_state_as_of_a_specific_date_formatted_YYYYMMDD(
    date, state, county
):
    cursor.execute(
        f"SELECT province_state AS State, county_city as County, date AS 'Totals as of Date', deaths AS Deaths FROM usa_covid19 WHERE date = '{date}' and province_state = '{state}' and county_city = '{county}'"
    )
    return cursor.fetchall()
