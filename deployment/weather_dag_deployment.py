from prefect import flow

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="git@github.com:HeinHtetNyi/weather-pipeline.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="dags/weather_dag.py:flow_function", # Specific flow to run
    ).deploy(
        name="weather-dag-deployment",
        work_pool_name="my-work-pool", # Work pool target
        cron="0 0 * * *",
    )
