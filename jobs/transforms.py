"""Transformations Spark partagées par le streaming et la recette locale."""
from pyspark.sql import functions as F, Window

def quality_condition():
    return (F.col('event_id').isNotNull() & (F.length('event_id')>0)
      & F.col('vehicle_id').isNotNull() & (F.length('vehicle_id')>0)
      & (F.col('event_ms')>0) & F.col('latitude').between(-90,90)
      & F.col('longitude').between(-180,180) & F.col('speed_kmh').between(0,220))

def enrich(events):
    return (events.filter(quality_condition()).dropDuplicates(['event_id'])
      .withColumn('event_time',F.timestamp_millis('event_ms'))
      .withColumn('day',F.date_format('event_time','yyyy-MM-dd'))
      .withColumn('speeding',F.col('speed_kmh')>80)
      .withColumn('outside_zone',~(F.col('latitude').between(33.50,33.66)
        & F.col('longitude').between(-7.72,-7.48))))

def with_segments(df):
    w=Window.partitionBy('vehicle_id').orderBy('event_ms','event_id')
    df=(df.withColumn('prev_lat',F.lag('latitude').over(w))
      .withColumn('prev_lon',F.lag('longitude').over(w))
      .withColumn('prev_ms',F.lag('event_ms').over(w)))
    a=(F.pow(F.sin(F.radians(F.col('latitude')-F.col('prev_lat'))/2),2)
      +F.cos(F.radians('latitude'))*F.cos(F.radians('prev_lat'))
      *F.pow(F.sin(F.radians(F.col('longitude')-F.col('prev_lon'))/2),2))
    return df.withColumn('segment_km',F.when(F.col('prev_ms').isNotNull()
      & ((F.col('event_ms')-F.col('prev_ms'))<=300000),
      6371*2*F.asin(F.sqrt(F.least(F.lit(1.),a)))).otherwise(0.))

def daily(s, df):
    df.createOrReplaceTempView('positions')
    return s.sql('''SELECT vehicle_id, day, sum(segment_km) distance_km,
      avg(speed_kmh) avg_speed_kmh, max(speed_kmh) max_speed_kmh,
      sum(CAST(speeding AS INT)) speeding_samples,
      sum(CAST(outside_zone AS INT)) outside_samples, count(*) samples,
      max(event_ms) event_ms FROM positions GROUP BY vehicle_id,day''')
