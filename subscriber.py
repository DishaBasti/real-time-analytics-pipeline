from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, desc
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
TOPICS = "viewership_north,viewership_south,viewership_east,viewership_west"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("RealTimeViewershipAnalytics") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define Schema for Incoming Kafka Data
schema = StructType([
    StructField("Event_ID", StringType(), True),
    StructField("Event_Type", StringType(), True),
    StructField("User_ID", StringType(), True),
    StructField("City", StringType(), True),
    StructField("State", StringType(), True),
    StructField("User_Type", StringType(), True),
    StructField("Timestamp", StringType(), True),
    StructField("Channel", StringType(), True),
    StructField("Program", StringType(), True),
    StructField("Channel_Type", StringType(), True),
    StructField("View_Min", IntegerType(), True),
    StructField("Session_Dur", IntegerType(), True),
    StructField("Preferred_Time", StringType(), True),
    StructField("Region", StringType(), True)
])

# Read stream from Kafka topics
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", TOPICS) \
    .load()

# Extract and parse JSON from Kafka 'value' field
df_parsed = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Convert Timestamp column to proper TimestampType
df_parsed = df_parsed.withColumn("Timestamp", col("Timestamp").cast(TimestampType()))

# ------------------ Real-Time Analytics ------------------

# 1. Top Channels by Total View Minutes (10-sec sliding window)
top_channels = df_parsed \
    .groupBy(window(col("Timestamp"), "10 seconds"), col("Channel")) \
    .sum("View_Min") \
    .withColumnRenamed("sum(View_Min)", "Total_View_Minutes") \
    .orderBy(desc("Total_View_Minutes"))

query1 = top_channels.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .queryName("TopChannels") \
    .start()

# 2. Regional Viewing Trends
regional_trends = df_parsed \
    .groupBy(window(col("Timestamp"), "10 seconds"), col("Region")) \
    .sum("View_Min") \
    .withColumnRenamed("sum(View_Min)", "Total_View_Minutes") \
    .orderBy(desc("Total_View_Minutes"))

query2 = regional_trends.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .queryName("RegionalTrends") \
    .start()

# 3. Count of Channel Switch Events (Event_Type = "channel_switch")
switch_events = df_parsed \
    .filter(col("Event_Type") == "channel_switch") \
    .groupBy(window(col("Timestamp"), "10 seconds")) \
    .count() \
    .withColumnRenamed("count", "Switch_Count")

query3 = switch_events.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .queryName("SwitchEvents") \
    .start()

# Keep the streaming queries running
spark.streams.awaitAnyTermination()
