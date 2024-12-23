## Description
This project is an end-to-end pipeline coded with Prefect.
- Fetching weather data from API
- Transforming data with Pandas
- Loading data into Postgres

## Database Schema
```
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY ,
    datetime TIMESTAMP WITHOUT TIME ZONE,
    temp FLOAT,
    feelslike FLOAT,
    sunrise TEXT,
    sunset TEXT,
    windspeed FLOAT,
    conditions TEXT
);
```

## To run a pipeline
```
  // Start Prefect Server Locally
  prefect start server

  // Create work-pool to deploy pipeline
  prefect work-pool create --type process my-work-pool

  // Start a worker
  prefect worker start --pool my-work-pool

  // Register our flow
  python dags/weather_dag.py

  // Deploy our flow
  python deployment/weather_dag_deployment.py

  // Run our deployment
  prefect deployment run 'weather_pipeline/weather-dag-deployment'
```
