"""Recette Spark locale : python tests/spark_smoke.py (pyspark 3.5.3 + Java 17)."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'jobs'))
from pyspark.sql import SparkSession
from transforms import enrich, with_segments, daily
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
s=SparkSession.builder.master('local[2]').appName('fleet-test').config('spark.sql.shuffle.partitions','2').config('spark.ui.enabled','false').getOrCreate()
s.sparkContext.setLogLevel('ERROR')
rows=[('a','V1',1735689600000,33.58,-7.60,80.),
      ('b','V1',1735689602000,33.58,-7.59,81.),
      ('b','V1',1735689602000,33.58,-7.59,81.),
      ('c','V1',1735689604000,34.,-7.59,0.),
      ('bad','V1',1735689606000,91.,-7.59,20.)]
df=s.createDataFrame(rows,'event_id string, vehicle_id string, event_ms long, latitude double, longitude double, speed_kmh double')
clean=enrich(df)
assert clean.count()==3
assert clean.filter('speeding').count()==1
assert clean.filter('outside_zone').count()==1
r=daily(s,with_segments(clean)).first()
assert r.samples==3 and r.speeding_samples==1 and r.outside_samples==1
assert 47 < r.distance_km < 48
points=s.createDataFrame([(0.,0.),(.1,.1),(10.,10.),(10.1,10.1)],['x','y'])
model=KMeans(k=2,seed=42).fit(VectorAssembler(inputCols=['x','y'],outputCol='features').transform(points))
assert len(model.clusterCenters())==2
s.stop(); print('SPARK_SMOKE_OK : qualité, doublons, alertes, distance, SQL, KMeans')
