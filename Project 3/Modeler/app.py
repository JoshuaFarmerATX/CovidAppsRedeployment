from flask import Flask
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric
from modeling import predictcases, predictdeaths
from modeling_us import predict_cases, predict_deaths

app = Flask(__name__)

# Import data
r = requests.get("https://api-app-pjblaypjta-uc.a.run.app/API/timeseries/usa")
response_dict = r.json()
df = pd.DataFrame.from_dict(response_dict)
df = df.rename(columns={"Totals as of Date": "Date"})
df["Date"] = pd.to_datetime(df["Date"]).dt.date
df["NewCases"] = df["Cases"] - df["Cases"].shift(1)
df["NewDeaths"] = df["Deaths"] - df["Deaths"].shift(1)

df_cases = df.loc[df["Cases"] >= 200_000]
df_deaths = df.loc[df["Date"] >= datetime.date(2020, 4, 8)]

df_cases_fb = df_cases[["Date", "NewCases"]].rename(
    columns={"Date": "ds", "NewCases": "y"}
)
df_deaths_fb = df_deaths[["Date", "NewDeaths"]].rename(
    columns={"Date": "ds", "NewDeaths": "y"}
)


@app.route("/")
def home():
    return "Working"


@app.route("/cases/<int:num>/")
def predictedcases(num):
    days = num
    return (predictcases(days)).to_json(orient="records", date_format="iso")


@app.route("/deaths/<int:num>/")
def predicteddeaths(num):
    days = num
    return (predictdeaths(days)).to_json(orient="records", date_format="iso")


@app.route("/states/cases/<usstate>/<int:num>/")
def predictedstatecases(usstate, num):
    days = num
    state = usstate
    return (predict_cases(state, days)).to_json(orient="records", date_format="iso")


@app.route("/states/deaths/<usstate>/<int:num>/")
def predictedstatedeaths(usstate, num):
    days = num
    state = usstate
    return (predict_deaths(state, days)).to_json(orient="records", date_format="iso")
