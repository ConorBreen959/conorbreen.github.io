from pytz import timezone
from datetime import datetime, timedelta
from skyfield import almanac
from skyfield.api import N, W, wgs84, load
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import seaborn as sb
from matplotlib import pyplot as plt


pio.renderers.default = "browser"

year = 2023
days = 365
if year % 4:
    days = 366

tz = timezone("Europe/Dublin")
ts = load.timescale()
now = tz.localize(datetime(2024, 1, 1))
eph = load('de421.bsp')
location = wgs84.latlon(53.3498 * N, 6.2603* W)
f = almanac.dark_twilight_day(eph, location)


first_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = first_midnight + timedelta(days=days)
t0 = ts.from_datetime(first_midnight)
t1 = ts.from_datetime(next_midnight)
times, events = almanac.find_discrete(t0, t1, f)

sunrise_df = pd.DataFrame(columns=["Date", "Event", "Starts", "Ends"])

def format_time(t):
    time_string = str(t.astimezone(tz))[:16]
    date_x, time_x = time_string.split(" ")
    date_object = datetime.strptime(date_x, "%Y-%m-%d").date()
    time_object = datetime.strptime(time_x, "%H:%M")
    time_in_seconds = timedelta(hours=time_object.hour, minutes=time_object.minute).seconds
    return date_object, time_object


for index, (t, e) in enumerate(zip(times, events)):
    event = almanac.TWILIGHTS[e]
    start_date, start_time = format_time(t)
    if index == len(times) - 1:
        end_date, end_time = format_time(t1)
    else:
        end_date, end_time = format_time(times[index + 1])
    event = event.replace("twilight", "dawn")
    if start_time.hour > 12:
        event = event.replace("dawn", "dusk")
    if end_date > start_date:
        first_df = pd.DataFrame(data={"Date": start_date, "Event": event, "Starts": start_time, "Ends": np.nan}, index=[0])
        next_df = pd.DataFrame(data={"Date": end_date, "Event": event, "Starts": np.nan, "Ends": end_time}, index=[0])
        sunrise_df = pd.concat([sunrise_df, first_df, next_df])
    else:
        df = pd.DataFrame(data={"Date": start_date, "Event": event, "Starts": start_time, "Ends": end_time}, index=[0])
        sunrise_df = pd.concat([sunrise_df, df])


sunrise_df = sunrise_df.reset_index(drop=True)


event_types = sunrise_df["Event"].drop_duplicates().tolist()
event_dfs = [sunrise_df[sunrise_df["Event"] == event_type] for event_type in event_types if event_type != "Night"]


fig = go.Figure()

for index, event_df in enumerate(event_dfs):
    name = event_df["Event"].tolist()[0]
    fill = "tonexty"
    if index == 0:
        fill = None
    fig.add_trace(go.Scatter(x=event_df["Date"], y=event_df["Starts"].replace(pd.NaT, np.nan), name=f"{name} starts", hovertemplate="%{y|%H:%M}"))
    fig.add_trace(go.Scatter(x=event_df["Date"], y=event_df["Ends"].replace(pd.NaT, np.nan), name=f"{name} ends", hovertemplate="%{y|%H:%M}<br>%{x}>"))
fig.show()


plt.figure(figsize=(50, 50))
sb.relplot(
    data=sunrise_df,
    kind="line",
    x="Date",
    y="Starts",
    hue="Event"
)

penguins = sb.load_dataset("penguins")
sb.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species")
