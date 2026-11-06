"""Recette Hudi locale, avec le bundle Hudi 0.15.0 dans --jars.
Exemple : spark-submit --jars hudi-spark3.5-bundle_2.12-0.15.0.jar tests/hudi_smoke.py
"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'jobs'))
from pyspark.sql import SparkSession
import common
from transforms import enrich
s=(SparkSession.builder.master('local[2]').appName('hudi-test')
 .config('spark.serializer','org.apache.spark.serializer.KryoSerializer')
 .config('spark.sql.extensions','org.apache.spark.sql.hudi.HoodieSparkSessionExtension')
 .config('spark.sql.catalog.spark_catalog','org.apache.spark.sql.hudi.catalog.HoodieCatalog')
 .config('spark.sql.shuffle.partitions','2').config('spark.ui.enabled','false').getOrCreate())
s.sparkContext.setLogLevel('ERROR')
with tempfile.TemporaryDirectory(prefix='fleet-hudi-') as directory:
    common.ROOT=Path(directory).as_uri()
    def frame(speed,ms):
        return enrich(s.createDataFrame([('same','V1',ms,33.58,-7.60,speed)],'event_id string, vehicle_id string, event_ms long, latitude double, longitude double, speed_kmh double'))
    common.hudi(frame(80.,1735689600000),'silver_positions','event_id','day')
    common.hudi(frame(90.,1735689601000),'silver_positions','event_id','day')
    result=s.read.format('hudi').load(f'{common.ROOT}/silver_positions')
    assert result.count()==1
    assert result.first().speed_kmh==90.
    assert result.first().speeding is True
s.stop(); print('HUDI_SMOKE_OK : upsert conserve une clé et met à jour la vitesse')
