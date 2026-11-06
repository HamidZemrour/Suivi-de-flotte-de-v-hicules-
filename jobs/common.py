import os
from pyspark.sql import SparkSession
ROOT='s3a://fleet'
def spark(name):
    return (SparkSession.builder.appName(name)
      .config('spark.serializer','org.apache.spark.serializer.KryoSerializer')
      .config('spark.sql.extensions','org.apache.spark.sql.hudi.HoodieSparkSessionExtension')
      .config('spark.sql.catalog.spark_catalog','org.apache.spark.sql.hudi.catalog.HoodieCatalog')
      .config('spark.hadoop.fs.s3a.endpoint','http://minio:9000')
      .config('spark.hadoop.fs.s3a.access.key',os.getenv('MINIO_ROOT_USER','fleetadmin'))
      .config('spark.hadoop.fs.s3a.secret.key',os.getenv('MINIO_ROOT_PASSWORD','fleetpassword123'))
      .config('spark.hadoop.fs.s3a.path.style.access','true')
      .config('spark.hadoop.fs.s3a.connection.ssl.enabled','false')
      .config('spark.sql.shuffle.partitions','4').getOrCreate())
def hudi(df,name,key,partition,mode='append'):
    (df.write.format('hudi').options(**{
      'hoodie.upsert.shuffle.parallelism':'4',
      'hoodie.insert.shuffle.parallelism':'4',
      'hoodie.table.name':name,'hoodie.datasource.write.table.type':'COPY_ON_WRITE',
      'hoodie.datasource.write.recordkey.field':key,
      'hoodie.datasource.write.precombine.field':'event_ms',
      'hoodie.datasource.write.partitionpath.field':partition,
      'hoodie.datasource.write.operation':'upsert',
      'hoodie.index.type':'GLOBAL_BLOOM',
      'hoodie.bloom.index.update.partition.path':'true',
      'hoodie.cleaner.commits.retained':'10'}).mode(mode).save(f'{ROOT}/{name}'))
