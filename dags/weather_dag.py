import requests
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from datetime import datetime, timedelta
from variables import Variables

variables = Variables()

@flow(log_prints=True, name="weather_pipeline")
def flow_function():
    weather_data = fetch_weather_api()
    if weather_data:
        final_data = transform_weather_data(weather_data)
        load_weather_data(final_data)

@task
def fetch_weather_api():
    try:
        today = datetime.today()
        start_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        print(start_date, end_date)
        url = f"""https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Myanmar/{start_date}/{end_date}?key={variables.DB_URL}"""
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
    except Exception as e:
        print("Error:", e)


@task
def transform_weather_data(raw_data):
    days = raw_data["days"]
    df = pd.DataFrame(days)
    df = df[["datetime", "temp", "feelslike", "sunrise", "sunset", "windspeed", "conditions"]]
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["temp"] = pd.to_numeric(df["temp"])
    df["feelslike"] = pd.to_numeric(df["feelslike"])
    df["sunrise"] = df["sunrise"]
    df["sunset"] = df["sunset"]
    df["windspeed"] = pd.to_numeric(df["windspeed"])
    df["conditions"] = df["conditions"]
    return df


@task
def load_weather_data(final_data):
    try:
        engine = create_engine(variables.DB_URL)
        with engine.connect() as conn:
            final_data.to_sql("weather_data", conn, if_exists="append", index=False)
        print("Data loaded successfully!")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        if 'engine' in locals() and engine:
            engine.dispose()


if __name__ == "__main__":
    flow_function()
