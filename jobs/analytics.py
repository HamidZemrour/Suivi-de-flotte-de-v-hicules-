import json, os
import boto3
from common import spark, ROOT, hudi
from transforms import with_segments, daily
from pyspark.sql import functions as F, Window
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
s=spark('fleet-analytics'); s.sparkContext.setLogLevel('WARN')
df=s.read.format('hudi').load(f'{ROOT}/silver_positions')
df=with_segments(df)
gold=daily(s,df)
hudi(gold,'gold_daily','vehicle_id,day','day')
# Zones d'arrêt : points à <= 5 km/h, métrique plane locale (Casablanca).
stops=(df.filter('speed_kmh <= 5').withColumn('x_km',F.col('longitude')*92.5).withColumn('y_km',F.col('latitude')*111.2))
features=VectorAssembler(inputCols=['x_km','y_km'],outputCol='features').transform(stops)
k=min(3,features.select('x_km','y_km').distinct().count())
zones=[]
if k>=2:
    model=KMeans(k=int(k),seed=42,maxIter=20).fit(features)
    model.write().overwrite().save(f'{ROOT}/models/stops')
    zones=[dict(zone=i,latitude=float(c[1]/111.2),longitude=float(c[0]/92.5)) for i,c in enumerate(model.clusterCenters())]
# Exports issus des tables Gold Hudi : snapshot pour Streamlit, jamais données simulées cachées.
g=s.read.format('hudi').load(f'{ROOT}/gold_daily')
latest=(df.withColumn('rn',F.row_number().over(Window.partitionBy('vehicle_id').orderBy(F.desc('event_ms'),F.desc('event_id')))).filter('rn=1'))
inc=df.filter('speeding OR outside_zone').orderBy(F.desc('event_ms')).limit(200)
s3=boto3.client('s3',endpoint_url='http://minio:9000',aws_access_key_id=os.getenv('MINIO_ROOT_USER','fleetadmin'),aws_secret_access_key=os.getenv('MINIO_ROOT_PASSWORD','fleetpassword123'))
# Les vues dernières positions/incidents sont aussi matérialisées en Gold Hudi.
for name,frame in [('gold_latest',latest.drop('rn')),('gold_incidents',df.filter('speeding OR outside_zone'))]:
    if not frame.isEmpty(): hudi(frame,name,'event_id' if name=='gold_incidents' else 'vehicle_id','day')
# Exports relus depuis Gold Hudi ; incident vide toléré avant la première alerte.
for key,frame in [('daily',g),('latest',s.read.format('hudi').load(f'{ROOT}/gold_latest')),('incidents',s.read.format('hudi').load(f'{ROOT}/gold_incidents').orderBy(F.desc('event_ms')).limit(200) if not inc.isEmpty() else inc)]:
    s3.put_object(Bucket='fleet',Key=f'exports/{key}.json',Body=('['+','.join(frame.toJSON().collect())+']').encode())
s3.put_object(Bucket='fleet',Key='exports/zones.json',Body=json.dumps(zones).encode())
s3.put_object(Bucket='fleet',Key='exports/status.json',Body=json.dumps({'updated_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'rows':df.count(),'clusters':k if k>=2 else 0}).encode())
s.stop()
