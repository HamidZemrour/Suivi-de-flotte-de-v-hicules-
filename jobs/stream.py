from common import spark, ROOT, hudi
from transforms import quality_condition, enrich
from pyspark.sql import functions as F, types as T
s=spark('fleet-stream'); s.sparkContext.setLogLevel('WARN')
schema=T.StructType([T.StructField('event_id',T.StringType()),T.StructField('vehicle_id',T.StringType()),T.StructField('event_ms',T.LongType()),T.StructField('latitude',T.DoubleType()),T.StructField('longitude',T.DoubleType()),T.StructField('speed_kmh',T.DoubleType())])
raw=(s.readStream.format('kafka').option('kafka.bootstrap.servers','kafka:9092').option('subscribe','positions').option('startingOffsets','earliest').option('failOnDataLoss','true').load())
def batch(df,batch_id):
    if df.isEmpty(): return
    # Bronze conserve payload et coordonnées Kafka ; les reprises réécrivent le même lot.
    (df.selectExpr('CAST(value AS STRING) payload','topic','partition','offset','timestamp').write.mode('overwrite').parquet(f'{ROOT}/bronze/batch={batch_id}'))
    events=df.select(F.from_json(F.col('value').cast('string'),schema).alias('e')).select('e.*')
    valid=quality_condition()
    events.filter(~F.coalesce(valid,F.lit(False))).write.mode('overwrite').json(f'{ROOT}/quarantine/batch={batch_id}')
    clean=enrich(events)
    if not clean.isEmpty(): hudi(clean,'silver_positions','event_id','day')
(raw.writeStream.foreachBatch(batch).option('checkpointLocation',f'{ROOT}/checkpoints/positions').trigger(processingTime='20 seconds').start().awaitTermination())
