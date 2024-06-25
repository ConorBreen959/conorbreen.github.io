from pytz import timezone
from datetime import datetime, timedelta
from skyfield import almanac
from skyfield.api import N, E, wgs84, load
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import plotly.graph_objects as go
import plotly.io as pio
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib as mpl


pio.renderers.default = "browser"

year = 2024
days = 366
if year % 4:
    days = 367

tz = timezone("Europe/Dublin")
ts = load.timescale()
now = tz.localize(datetime(year, 1, 1))
eph = load('de421.bsp')

city = "Dublin, IE"
geolocator = Nominatim(user_agent="MyApp")
location = geolocator.geocode(city)

location = wgs84.latlon(location.latitude * N, location.longitude * E)
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

for index, (t, e) in enumerate(zip(times[0:49], events[0:49])):
    event = almanac.TWILIGHTS[e]
    next_event = list(events).index(e, index+1)
    print(event)
    print(almanac.TWILIGHTS[events[next_event]])


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


event_types = {
    'Astronomical dawn': "#785a08",
    'Nautical dawn': "#d29e0e",
    'Civil dawn': "#f4ca58",
    'Day': "#fae7b2",
    'Civil dusk': "#f4ca58",
    'Nautical dusk': "#d29e0e",
    'Astronomical dusk': "#785a08",
    'Night': "#261a03",
}

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(9, 7), dpi=1000)
for event_type, fill in event_types.items():
    event_df = sunrise_df[sunrise_df["Event"] == event_type]
    if 
    ax.fill_between(x="Date", y1="Starts", y2=, data=event_df, color=fill)
plt.savefig("my_fig.png")






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
