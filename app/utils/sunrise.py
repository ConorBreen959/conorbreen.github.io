from pytz import timezone
from datetime import datetime, timedelta
from skyfield import almanac
from skyfield.api import N, W, wgs84, load
import pandas as pd


year = 2023
days = 365
if year % 4:
    days = 366

tz = timezone("Europe/Dublin")
now = tz.localize(datetime(2024, 1, 1))
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = midnight + timedelta(days=366)

ts = load.timescale()
t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)
eph = load('de421.bsp')
bluffton = wgs84.latlon(40.8939 * N, 83.8917 * W)
f = almanac.dark_twilight_day(eph, bluffton)
times, events = almanac.find_discrete(t0, t1, f)

sunrise_df = pd.DataFrame(columns=["Date", "Time", "Type"])

previous_e = f(t0).item()
for t, e in zip(times, events):
    time_string = str(t.astimezone(tz))[:16]
    date, time = time_string.split(" ")
    twilight = almanac.TWILIGHTS[e]
    if previous_e < e:
        twilight_type = f"{twilight} starts"
    else:
        twilight_type = f"{twilight} ends"
    print(f"{time_string} {twilight_type}")
    previous_e = e
    df = pd.DataFrame(data={"Date": date, "Time": datetime.strptime(f"{time}", "%H:%M"), "Type": twilight_type}, index=[0])
    sunrise_df = pd.concat([sunrise_df, df])


fig = px.line(sunrise_df, x="Date", y="Time", color="Type")
fig.show()
