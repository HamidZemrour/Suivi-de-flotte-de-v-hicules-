from datetime import datetime, timedelta, timezone
import io, json, os
import boto3
from airflow.decorators import dag, task
@dag(schedule='@daily', start_date=datetime(2025,1,1),catchup=False,default_args={'retries':2,'retry_delay':timedelta(minutes=2)},tags=['ISSE-05'])
def daily_driving_report():
    @task
    def quality_and_report():
        s3=boto3.client('s3',endpoint_url='http://minio:9000',aws_access_key_id=os.environ['MINIO_ROOT_USER'],aws_secret_access_key=os.environ['MINIO_ROOT_PASSWORD'])
        status=json.loads(s3.get_object(Bucket='fleet',Key='exports/status.json')['Body'].read())
        age=(datetime.now(timezone.utc)-datetime.fromisoformat(status['updated_at'])).total_seconds()
        if age>900: raise ValueError('Export Gold trop ancien (>15 minutes)')
        rows=json.loads(s3.get_object(Bucket='fleet',Key='exports/daily.json')['Body'].read())
        if not rows or any(r['distance_km']<0 or r['samples']<=0 for r in rows):
            raise ValueError('Contrôle qualité Gold échoué')
        # Rapport de la journée précédente UTC ; zéro ligne est explicite.
        from airflow.operators.python import get_current_context
        day=get_current_context()['data_interval_start'].strftime('%Y-%m-%d')
        selected=[r for r in rows if r['day']==day]
        report={'day':day,'vehicles':len(selected),'distance_km':sum(r['distance_km'] for r in selected),'speeding_samples':sum(r['speeding_samples'] for r in selected),'data':selected}
        s3.put_object(Bucket='fleet',Key=f'reports/{day}.json',Body=json.dumps(report).encode())
        return {'day':day,'vehicles':len(selected)}
    quality_and_report()
daily_driving_report()
