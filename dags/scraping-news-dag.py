from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from google.oauth2 import service_account
import yaml

with open("dags/source/list_tables.yaml") as f:
    list_tables = yaml.safe_load(f)

@dag()
def scraping_news_dag():
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")

    for table in list_tables:
        spark_submit = SparkSubmitOperator(
            application = f"/spark-scripts/spark-{table}.py",
            conn_id = "spark_main",
            task_id = f"spark_load_task_{table}",
        )

        @task(task_id=f"scraping_{table}")
        def scrapping(table_name):
            from source import nyt, cnn
            module_map = {"cnn": cnn, "nyt": nyt}
            df = module_map[table_name].main()
            df.to_csv(f"/opt/airflow/data/{table}.csv")
        
        @task(task_id=f"load_bigquery_{table}")
        def load_bigquery(table_name):
            try:
                import pandas as pd
                df = pd.read_csv(f"/opt/airflow/data/{table_name}_spark.csv", index_col=0)
                print(df)
                df.columns = df.columns.str.replace('.', '_', regex=True)
                print(df.columns)
                credentials = service_account.Credentials.from_service_account_file('/opt/airflow/cred/service_account.json')
                project_id = 'final-project-450410'
                dataset_ref = f"news.{table_name}"

                df.to_gbq(destination_table=dataset_ref, project_id=project_id, credentials=credentials, if_exists="replace")

            except Exception as e:
                print(f"Data Load Error: {e}")
        
        start_task >> scrapping(table) >> spark_submit >> load_bigquery(table) >> end_task

scraping_news_dag() 
