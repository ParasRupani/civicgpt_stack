#!/usr/bin/env python
import os
import glob
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_date, size, split, round as spark_round
from pyspark.sql.types import FloatType, StringType
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# ========= Setup =========
nltk.download('vader_lexicon')

# Paths
RAW_DIR = "/opt/airflow/data/raw/news/"
PROCESSED_DIR = "/opt/airflow/data/processed/"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ========= Spark Session =========
spark = SparkSession.builder \
    .appName("CivicGPT+ Local News Transformer") \
    .getOrCreate()

# ========= VADER Sentiment =========
analyzer = SentimentIntensityAnalyzer()

def vader_sentiment(text):
    try:
        return float(analyzer.polarity_scores(text)['compound'])
    except:
        return 0.0

def vader_label(text):
    try:
        score = analyzer.polarity_scores(text)['compound']
        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"
    except:
        return "neutral"

compound_udf = udf(vader_sentiment, FloatType())
label_udf = udf(vader_label, StringType())

# ========= Process each file =========
json_files = glob.glob(os.path.join(RAW_DIR, "*.json"))

for json_path in json_files:
    filename = os.path.splitext(os.path.basename(json_path))[0]
    print(f"📥 Processing: {filename}")

    # Read single file
    df_raw = spark.read.option("multiLine", True).json(json_path)

    # Transform
    df_cleaned = df_raw \
        .withColumn("published_date", to_date(col("published"))) \
        .withColumn("word_count", size(split(col("summary"), " "))) \
        .withColumn("sentiment_score", spark_round(compound_udf(col("summary")), 3)) \
        .withColumn("sentiment_label", label_udf(col("summary")))

    # Write to a temp parquet directory
    temp_dir = os.path.join(PROCESSED_DIR, f"{filename}_tmp")
    df_cleaned.coalesce(1).write.mode("overwrite").parquet(temp_dir)

    # Find and rename the part file
    part_file = glob.glob(os.path.join(temp_dir, "part-*.parquet"))[0]
    final_path = os.path.join(PROCESSED_DIR, f"{filename}.parquet")
    shutil.move(part_file, final_path)
    shutil.rmtree(temp_dir)

    print(f"✅ Saved: {final_path}")

# ========= Done =========
spark.stop()
print("🏁 All files processed.")
