from flask import Flask, render_template, request
import pandas as pd
import os
import sys
import subprocess

from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from pyspark.sql.types import *

app = Flask(__name__)

# Sparkセッションの初期化
spark = SparkSession.builder.appName("PythonSQL").master("local[*]").getOrCreate()

# 初期表示データの読み込み
df = spark.sql("SELECT * FROM simple_table")

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_results = []
    filter_value = ""

    if request.method == "POST":
        filter_value = request.form.get("city_filter", "")
        if filter_value:
            # Spark SQLを使ってデータをフィルタリング
            sql_query = f"SELECT * FROM simple_table WHERE col3 = '{filter_value}'"
            filtered_df = spark.sql(sql_query)
    else:
        filtered_df = df
            
    # Pandas DataFrameに変換してWeb表示用に整形
    filtered_results = filtered_df.toPandas().to_dict('records')
    
    return render_template("index.html", results=filtered_results, filter_value=filter_value)

# メイン
if __name__ == '__main__':
    app.static_folder = os.environ['HOME'] + '/static'
    # app.template_folder = os.environ['HOME'] + '/templates'

    try:
        app.run(host = '127.0.0.1', port = int(os.environ['CDSW_APP_PORT']))
    except Exception as e:
        print(f"ERROR: unable to run application:\n {str(e)}")
