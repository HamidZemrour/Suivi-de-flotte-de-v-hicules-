from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from airflow.decorators import dag, task
@dag(schedule='*/2 * * * *',start_date=datetime(2025,1,1),catchup=False,max_active_runs=1,default_args={'retries':2,'retry_delay':timedelta(seconds=30)},tags=['ISSE-05'])
def refresh_gold():
    @task(execution_timeout=timedelta(minutes=20))
    def spark_aggregates_and_kmeans():
        req=Request('http://spark-batch:8090/run',data=b'',method='POST')
        with urlopen(req,timeout=1150) as response:
            return response.read().decode()
    spark_aggregates_and_kmeans()
refresh_gold()
