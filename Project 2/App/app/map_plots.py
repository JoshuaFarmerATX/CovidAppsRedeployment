#%%
import plotly.graph_objects as go
import plotly.offline
import plotly
import pandas as pd
import datetime as dt
import os
import json

connection_string = "mysql+pymysql://root:ehaarmanny@/Covid?unix_socket=/cloudsql/project2-270717:us-central1:covid2019"

#%%
def load_data():

    df = pd.read_sql("SELECT * FROM plotting", con=connection_string, index_col="index")
    return df


#%%
raw_df = load_data()
date_series = raw_df["date"].unique()
colorscale_dict = {"confirmed": "Blues", "deaths": "Reds", "recovered": "Greens"}

#%%
def create_traces(
    fig,
    confirmed_deaths_recovered,
    df=raw_df,
    date_series=date_series,
    colorscale_dict=colorscale_dict,
):
    for date in date_series:
        trace_df = df[df["date"] == date]
        fig.add_trace(
            dict(
                type="choropleth",
                locations=trace_df["iso3"],
                locationmode="ISO-3",
                z=trace_df[confirmed_deaths_recovered],
                colorscale=colorscale_dict[confirmed_deaths_recovered],
            )
        )

    fig.update_layout(
        title={
            "text": f"COVID-19 {confirmed_deaths_recovered.title()} as of {max(date_series)}",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        autosize=True,
        geo={
            "scope": "world",
            "projection": {"type": "natural earth"},
            "oceancolor": "#3399ff",
            "showcountries": True,
        },
        height=900,
    )


#%%
def create_slider(fig, confirmed_deaths_recovered, date_series=date_series):
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[
                # make ith trace visible
                {"visible": [date == i for date in range(len(fig.data))]},
            ],
            label=str(date_series[i]),
        )
        steps.append(step)

    sliders = [
        dict(
            active=len(fig.data) - 1,
            currentvalue={"prefix": "Date: "},
            pad={"t": 50},
            steps=steps,
        )
    ]

    fig.update_layout(sliders=sliders)


#%%
def create_map(confirmed_deaths_recovered):
    map_fig = go.Figure()
    create_traces(map_fig, confirmed_deaths_recovered)
    create_slider(map_fig, confirmed_deaths_recovered)
    return plotly.offline.plot(map_fig, include_plotlyjs=False, output_type="div")


#%%
# print(create_map("confirmed"))

# if __name__ == "__main__":
#     print(create_map("confirmed"))
#     print(create_map("deaths"))
#     print(create_map("recovered"))


# %%
