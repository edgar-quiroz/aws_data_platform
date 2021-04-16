import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import DataFrame, Row
import datetime
from awsglue import DynamicFrame

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "cdp-data-lake-datacatalog-stack-streaming-database", additionalOptions = {"startingOffsets": "earliest"}, stream_batch_time = 100 seconds, stream_type = Kafka, table_name = "kafka-employees"]
## @return: DataSource0
## @inputs: []
data_frame_DataSource0 = glueContext.create_data_frame.from_catalog(database = "cdp-data-lake-datacatalog-stack-streaming-database", table_name = "kafka-employees", transformation_ctx = "DataSource0", additional_options = {"startingOffsets": "earliest"})
def processBatch(data_frame, batchId):
    if (data_frame.count() > 0):
        DataSource0 = DynamicFrame.fromDF(data_frame, glueContext, "from_data_frame")
        ## @type: ApplyMapping
        ## @args: [mappings = [("id", "int", "id", "int"), ("first_name", "string", "first_name", "string"), ("last_name", "string", "last_name", "string"), ("email", "string", "email", "string")], transformation_ctx = "Transform0"]
        ## @return: Transform0
        ## @inputs: [frame = DataSource0]
        Transform0 = ApplyMapping.apply(frame = DataSource0, mappings = [("id", "int", "id", "int"), ("first_name", "string", "first_name", "string"), ("last_name", "string", "last_name", "string"), ("email", "string", "email", "string")], transformation_ctx = "Transform0")
        ## @type: DataSink
        ## @args: [database = "cdp-data-lake-datacatalog-stack-company-database", stream_batch_time = "100 seconds", table_name = "employees", transformation_ctx = "DataSink0"]
        ## @return: DataSink0
        ## @inputs: [frame = Transform0]

        DataSink0 = glueContext.write_dynamic_frame.from_catalog(frame = Transform0, database = "cdp-data-lake-datacatalog-stack-company-database", table_name = "employees", transformation_ctx = "DataSink0")
glueContext.forEachBatch(frame = data_frame_DataSource0, batch_function = processBatch, options = {"windowSize": "100 seconds", "checkpointLocation": args["TempDir"] + "/checkpoint/"})
job.commit()