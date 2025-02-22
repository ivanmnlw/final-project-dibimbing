from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from google.oauth2 import service_account
from datetime import datetime

@dag()
def extract_sp500():
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")

    @task()
    def load_to_bigquery():
        try:
            import pandas as pd
            df = pd.read_csv(f"/opt/airflow/data/sp500_1month.csv")
            print(df)
            df["Date"] = df["Date"].apply(lambda x: datetime.strptime(x, "%m/%d/%Y"))
            df = df.rename(columns={"Close/Last": "Close"})
            print(df)
            credentials = service_account.Credentials.from_service_account_file('/opt/airflow/cred/service_account.json')
            project_id = 'final-project-450410'
            dataset_ref = f"news.sp500"

            df.to_gbq(destination_table=dataset_ref, project_id=project_id, credentials=credentials, if_exists="replace")

        except Exception as e:
            print(f"Data Load Error: {e}")
    
    start_task >> load_to_bigquery() >> end_task

extract_sp500()
